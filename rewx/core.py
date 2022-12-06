"""
https://medium.com/@sweetpalma/gooact-react-in-160-lines-of-javascript-44e0742ad60f
"""
import functools
from threading import Lock

import wx
import wx.lib.inspection # Needed for the orphan remover
from inspect import isclass

from rewx.dispatch import mount, update
from rewx.widgets import mount as _mount
from rewx.widgets import update as _update

mount.merge_registries(_mount._registry)
update.merge_registries(_update._registry)



def wsx(f):
    def convert(spec: list):
        type = spec[0]
        props = spec[1]
        children = spec[2:]
        return create_element(type, props, children=list(map(convert, children)))
    # being used as a decorator
    if callable(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            result = f(*args, **kwargs)
            return convert(result)
        return inner
    else:
        return convert(f)


def create_element(type, props, children=None):
    element = {
        'type': type,
        'props': props
    }
    if children:
        if not isinstance(children, list):
            raise Exception('Children must be a list!')
        element['props']['children'] = children
    return element



def updatewx(instance, props):
    if isinstance(instance, wx.StaticText):
        instance: wx.StaticText = instance
        if props.get('on_click'):
            instance.Unbind(wx.EVT_LEFT_DOWN)
            instance.Unbind(wx.EVT_LEFT_DCLICK)
            instance.Bind(wx.EVT_LEFT_DOWN, props.get('on_click'))
            instance.Bind(wx.EVT_LEFT_DCLICK, props.get('on_click'))
        else:
            instance.Unbind(wx.EVT_LEFT_DCLICK)
            instance.Unbind(wx.EVT_LEFT_DOWN)
        instance.SetLabel(props.get('value', ''))
    elif isinstance(instance, wx.Panel):
        instance: wx.Panel = instance
        sizer: wx.BoxSizer = instance.GetSizer()
        sizer.SetOrientation(props.get('orient', wx.VERTICAL))
    return instance


def patch(dom: wx.Window, vdom) -> wx.Window:
    """
    Diffing and reconciliation.
    """
    parent = dom.GetParent()
    try:
        # if parent:
        #     parent.Freeze()
        if not isclass(vdom['type']):
            # because stateless functions are just opaque wrappers
            # they have no relevant diffing logic -- there is no
            # associated top-level WX element produced from a SFC, only
            # their inner contents matter. As such, we evaluate it and
            # push the result back into `patch`
            return patch(dom, vdom['type'](vdom['props']))
        if isclass(vdom['type']) and issubclass(vdom['type'], Component):
            return Component.patch_component(dom, vdom)
        elif not isinstance(dom, vdom['type']):
            # Create a new dom Window. The old dom Window will be Destroy()ed by reconciliation.
            newdom = render(vdom, parent)
        elif isinstance(dom, vdom['type']) and getattr(dom, 'self_managed', False):
            # self-managed components manage their children by hand rather than
            # automatically via the rewx dom. As such, we don't perform any child
            # diffing or reconciliation operations for them. The virtualdom will NOT
            # match the actual dom for these widgets.
            #
            # Background: These components are legacy/vanilla wx components the user created
            # which have been introduced into rewx land through custom mount/update handlers.
            # These are commonly used while porting over existing code or for wx components
            # which are sufficiently cranky about their child management.
            update(vdom, dom)
            newdom = dom
        elif isinstance(dom, vdom['type']):
            update(vdom, dom)
            # We have to treat Windows with Sizers differently from Windows without Sizers.
            # The problem is that Sizer.Insert() puts the child in the position in the Sizer,
            # but the child gets appended to the dom.GetChildren() list.
            # So then the vdom and the dom.GetChildren() disagree.
            sizer = dom.GetSizer()
            if sizer is None:
                pool = {f'__index_{index}': child for index, child in enumerate(dom.GetChildren())}
                for index, child in enumerate(vdom['props'].get('children', [])):
                    key = f'__index_{index}'
                    if key in pool:
                        domchild = pool[key]
                        # patch will attempt to update in place. If successful, domchild is returned.
                        # Maybe patch returns a different domchild, possibly a different type of domchild.
                        newdomchild = patch(domchild, child)
                        if newdomchild is not domchild:
                            # TODO
                            # If the Window doesn't have a Sizer, we can only append children.
                            # This child will be positioned incorrectly.
                            #
                            # Currently the Frame doesn't have a Sizer.
                            #
                            # Maybe we should require that all Windows which can have children
                            # must have a Sizer.
                            domchild.Destroy()
                            dom.AddChild(
                                newdomchild,
                                child['props'].get('proportion', 0),
                                child['props'].get('flag', 0),
                                child['props'].get('border', 0)
                            )
                        del pool[key]
                    else:
                        inst = render(child, dom)
                        dom.AddChild(
                            inst,
                            child['props'].get('proportion', 0),
                            child['props'].get('flag', 0),
                            child['props'].get('border', 0)
                        )
                # any keys which haven't been removed in the
                # above loop represent wx.Objects which are no longer
                # part of the virtualdom and should thus be removed.
                for key, orphan in pool.items():
                    # Debugging InspectionFrame gets lumped in with the
                    # top-level hierarchy. We want to leave this alone as
                    # it's there for debugging and not part of the actual
                    # declared component tree
                    if not isinstance(orphan, wx.lib.inspection.InspectionFrame):
                        orphan.Destroy()
            else: # This dom Window has a Sizer
                # TODO What about child items which are not Window, instead are Sizer or Spacer?
                pool = {f'__index_{index}': child.GetWindow() for index, child in enumerate(sizer.GetChildren())}
                for index, child in enumerate(vdom['props'].get('children', [])):
                    # TODO 'key' props like in React.
                    #       Otherwise inserting a new child or deleting a child causes all the later
                    #       children to be re-rendered.
                    key = f'__index_{index}'
                    if key in pool:
                        domchild = pool[key]
                        # patch will attempt to update in place. If successful, domchild is returned.
                        # Maybe patch returns a different domchild, possibly a different type of domchild.
                        newdomchild = patch(domchild, child)
                        if newdomchild is not domchild:
                            # Only a Sizer can Insert() at a position.
                            domchild.Destroy()
                            sizer.Insert(
                                index,
                                newdomchild,
                                child['props'].get('proportion', 0),
                                child['props'].get('flag', 0),
                                child['props'].get('border', 0)
                            )
                            # We can't use
                            # https://docs.wxpython.org/wx.Sizer.html#wx.Sizer.Replace
                            # because it doesn't allow us to set proportion, flag, border.
                        del pool[key]
                    else:
                        # If we're not updating, we're appending to the end of the children list.
                        inst = render(child, dom)
                        sizer.Add(
                            inst,
                            child['props'].get('proportion', 0),
                            child['props'].get('flag', 0),
                            child['props'].get('border', 0)
                        )
                # any keys which haven't been removed in the
                # above loop represent wx.Objects which are no longer
                # part of the virtualdom and should thus be removed.
                # TODO What about items which are not Window, instead are Sizer or Spacer?
                for key, orphan in pool.items():
                    # Debugging InspectionFrame gets lumped in with the
                    # top-level hierarchy. We want to leave this alone as
                    # it's there for debugging and not part of the actual
                    # declared component tree
                    if not isinstance(orphan, wx.lib.inspection.InspectionFrame):
                        orphan.Destroy()
                # https://docs.wxpython.org/wx.Window.html#wx.Window.Layout
                dom.Layout()

            newdom = dom
        else:
            raise Exception("unexpected case!")
        return newdom
    finally:
        # TODO: we sometimes call parent.Thaw() when
        # parent isn't frozen. I think this has something
        # to do with the child removal case. Not sure tho
        # if parent and parent.IsFrozen():
        #     parent.Thaw()
        pass


class Component:
    def __init__(self, props):
        self.props = props
        self.state = None
        # this gets set dynamically once mounted / instantiated
        self.base = None
        self._lock = Lock()

    @classmethod
    def render_component(cls, vdom, parent=None):
        if cls.__name__ == vdom['type'].__name__:
            instance = vdom['type'](vdom['props'])
            instance.base = render(instance.render(), parent)
            instance.base._instance = instance
            instance.base._key = vdom['props'].get('key', None)
            instance.component_did_mount()

            return instance.base
        else:
            # TODO: what are the cases where this would be hit..?
            return render(vdom['type'](vdom['props']), parent)

    @classmethod
    def patch_component(cls, dom, vdom):
        parent = dom.GetParent()
        # TODO: is any of this right..?
        if hasattr(dom, '_instance') and type(dom._instance).__name__ == vdom['type'].__name__:
            dom._instance.props = vdom['props']
            updated = patch(dom, dom._instance.render())
            updated._instance.component_did_update(updated._instance.props)
            return updated

        if cls.__name__ == vdom['type'].__name__:
            return cls.render_component(vdom, parent)
        else:
            return patch(dom, vdom['type'](vdom['props']))


    def component_did_mount(self):
        pass

    def component_will_unmount(self):
        pass

    def component_did_update(self, next_state):
        pass

    def render(self):
        return None

    def set_state(self, next_state):
        with self._lock:
            prev_state = self.state
            self.state = next_state
            p = self.base
            while p.GetParent() != None:
                p = p.GetParent()
            p.Freeze()
            patch(self.base, self.render())
            p.Thaw()

def isfunction(element):
    return callable(element['type']) and not isclass(element['type'])

def render(element, parent:wx.Window) -> wx.Window:
    """
    Create a new dom Window and mount it for the first time.
    """
    if isclass(element['type']) and issubclass(element['type'], wx.Object):
        instance = mount(element, parent)
        if element['props'].get('ref'):
            element['props'].get('ref').update_ref(instance)
        for child in element['props'].get('children', []):
            # Implementation Note:
            # Stateless Function Components are just simple convenience wrappers for bundling up
            # related Elements in in rewx. They have no directly instantiatable object type.
            # Effectively, it's just like a Thunked blob of Elements. As such, when we encounter
            # a SFC, to get the actual rewx Elements, we evaluate the function and its props thus
            # yielding an Element Tree we can actually mount / render.
            if isfunction(child):
                # evaluating the SFC to get the actual child contents
                child = child['type'](child['props'])
            sizer = instance.GetSizer()
            if not sizer:
                render(child, instance)
            else:
                sizer.Add(
                    render(child, instance),
                    child['props'].get('proportion', 0),
                    child['props'].get('flag', 0),
                    child['props'].get('border', 0)
                )
        if isinstance(instance, wx.Frame):
            instance.Layout()
        return instance
    elif type(element['type']) == type:
        return element['type'].render_component(element, parent)
    elif callable(element['type']):
        # stateless functional component
        return render(element['type'](element['props']), parent)
    else:
        # TODO: rest of this message
        raise TypeError(f'''
            An unknown type ("{element['type']}") was supplied as a renderable
            element.
        ''')

class Ref:
    def __init__(self):
        self.instance = None

    def update_ref(self, instance):
        self.instance = instance


if __name__ == '__main__':
    statictext = wx.StaticText

    foo_elm = create_element('block', {}, children=[
        create_element('statictext', {'value': 'Hey there, world!'}),
        create_element('statictext', {'value': 'Hey there, again!'}),
        create_element('block', {'orient': wx.HORIZONTAL}, children=[
            create_element('statictext', {'value': 'One'}),
            create_element('statictext', {'value': ' and Two!'}),
        ])
    ])

    foo_elm1 = create_element('block', {}, children=[
        create_element('statictext', {'value': 'One'}),
        create_element('statictext', {'value': 'Two'})
    ])

    foo_elm2 = create_element('block', {'orient': wx.HORIZONTAL}, children=[
        create_element('statictext', {'value': 'Two'}),
        create_element('statictext', {'value': 'One'}),
    ])

    # foo_elm3 = create_element(Foo, {'item1': 'HELLOOOOO'})
    # foo_elm4 = create_element(Bar, {})
    #
    # foo_elm5 = create_element(Bar, {'item1': 'HELLOOOOO'})
    # foo_elm6 = create_element(Foo, {'item1': 'BYeeeee'})

    # basic_app('My Hello App', foo_elm)

    app = wx.App()
    import wx.lib.inspection
    wx.lib.inspection.InspectionTool().Show()
    frame = wx.Frame(None, title='Test re-wx')
    frame.SetSize((570, 520))
    thing = render(create_element(statictext, {'label': 'Two'}), frame)
    # thing = patch(thing, foo_elm6)
    # t = Thread(target=andthen, args=(thing, foo_elm6))
    # t.start()
    box = wx.BoxSizer(wx.VERTICAL)
    box.Add(thing, 1, wx.EXPAND)
    frame.SetSizer(box)
    frame.Show()
    # frame.Fit()

    for child in frame.GetChildren():
        for ccc in child.GetChildren():
            for cc in ccc.GetChildren():
                cc.Layout()
            ccc.Layout()
        child.Layout()
    app.MainLoop()


