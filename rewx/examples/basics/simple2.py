"""
https://medium.com/@sweetpalma/gooact-react-in-160-lines-of-javascript-44e0742ad60f
"""
import datetime
import wx
from threading import Thread
from uuid import uuid4

from rewx.rewx import wsx


def create_element(type, props, children=None):
    element = {
        'type': type,
        'props': props
    }
    if children:
        element['props']['children'] = children
    return element

def textctrl2wx(element, parent):
    text = wx.TextCtrl(parent)
    text.SetLabel(element['props'].get('label'))
    if element['props'].get('on_click'):
        text.Bind(wx.EVT_LEFT_DOWN, element['props'].get('on_click'))
    text._type = element['type']
    return text

def statictext2wx(element, parent):
    text = wx.StaticText(parent)
    if element['props'].get('name'):
        text.SetName(element['props']['name'])
    text.SetLabel(element['props'].get('value'))
    if element['props'].get('on_click'):
        text.Bind(wx.EVT_LEFT_DOWN, element['props'].get('on_click'))
    text._type = element['type']
    return text

def block2wx(element, parent):
    panel = wx.Panel(parent)
    panel._type = element['type']
    box = wx.BoxSizer((element.get('props') or {}).get('orient', wx.VERTICAL))
    # for elm in element['props']['children']:
    #     wx_instance = render(elm, panel)
    #     box.Add(wx_instance, elm['props'].get('proportion', 0),
    #             elm['props'].get('flag', 0),
    #             elm['props'].get('border', 0))
    panel.SetSizer(box)
    return panel


def vanilla():
    return create_element('block', {}, children=[
        create_element('statictext', {'value': 'Hello'})
    ])


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


def patch(dom: wx.Window, vdom):
    parent = dom.GetParent()
    try:
        parent.Freeze()
        # issubclass(vdom['type'], Component)
        if type(vdom['type']) == type:
            return Component.Patch(dom, vdom)
        # isstatelessfunctional
        if callable(vdom['type']):
            return patch(dom, vdom['type'](vdom['props']))
        if vdom['type'] != dom._type:
            for child in dom.GetChildren():
                dom.RemoveChild(child)
                child.Destroy()
            dom.Destroy()
            newdom = render(vdom, parent)
        elif vdom['type'] == dom._type:
            updatewx(dom, vdom['props'])
            pool = {f'__index_{index}': child for index, child in enumerate(dom.GetChildren())}
            for index, child in enumerate(vdom['props'].get('children', [])):
                key = f'__index_{index}'
                if key in pool:
                    patch(pool[key], child)
                else:
                    parent.RemoveChild(pool[key])
                    render(child, parent)
            newdom = dom
        p = parent
        while p:
            p.Layout()
            p = p.GetParent()
        return newdom
    finally:
        parent.Thaw()





class Component:
    def __init__(self, props):
        self.props = props
        self.state = None
        # this gets set dynamically once mounted / instantiated
        self.base = None

    @classmethod
    def Render(cls, vdom, parent=None):
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
    def Patch(cls, dom, vdom):
        parent = dom.GetParent()
        # TODO: is any of this right..?
        if hasattr(dom, '_instance') and type(dom._instance).__name__ == vdom['type'].__name__:
            return patch(dom, dom._instance.render())
        if cls.__name__ == vdom['type'].__name__:
            return cls.Render(vdom, parent)
        else:
            return patch(dom, vdom['type'](vdom['props']))


    def component_did_mount(self):
        pass

    def render(self):
        return None

    def set_state(self, next_state):
        prev_state = self.state
        self.state = next_state
        patch(self.base, self.render())


class Foo(Component):
    def __init__(self, props):
        super().__init__(props)
        self.timer = None
        self.state = {
            'value': datetime.datetime.now()
        }

    def component_did_mount(self):
        print('hello from foo!')
        self.timer = Thread(target=self.clock)
        self.timer.start()

    def clock(self):
        import time
        while True:
            time.sleep(1)
            print('still updating!', time.time())
            wx.CallAfter(self.set_state, {'value': datetime.datetime.now()})

    def render(self):
        return create_element('block', {}, children=[
            create_element('statictext', {'value': self.props['item1']}),
            create_element('statictext', {'value': self.state['value'].strftime('%I:%M:%S')})
        ])


class Bar(Component):
    def __init__(self, props):
        super().__init__(props)
        self.timer = None
        self.state = {
            'value': str(uuid4())
        }

    def on_click(self, event):
        import time
        s = time.time()
        self.set_state({'value': str(uuid4())})
        print('total:',  datetime.datetime.now())

    def render(self):
        return wsx(
            ['block', {},
             [Foo, {'item1': 'Whatup, nigga?'}],
             ['statictext', {'value': self.state['value'], 'on_click': self.on_click}],
             [my_thing2, {'name': self.state['value']}],
             ['statictext', {'value': 'Five'}]]
        )


def my_div(props):
    return wsx(['block', {'props': props['orient']}])

def my_thing(props):
    """
    TODO: Text stateless functional components
    """
    return create_element('my_div', {'orient': wx.HORIZONTAL}, children=[
        create_element('statictext', {'value': 'Your name is: '}),
        create_element('statictext', {'value': props['name']})
    ])


def my_thing2(props):
    return wsx(
        ['my_div', {},
         ['statictext', {'value': 'Your name is: '}],
         ['textctrl', {'label': 'one two'}],
         ['statictext', {'value': props['name']}]]
    )



class Clock(Component):
    def __init__(self, props):
        super().__init__(props)
        self.state = {
            'time': datetime.datetime.now()
        }

    def render(self):
        return wsx(
          ['block', {},
           ['textctrl', {'label': 'one fasdf'}],
           ['statictext', {'value': self.state['time'].strftime('%I:%M:%S'),
                           'name': 'ClackFace',
                           'proporton': 1,
                           'flag': wx.CENTER | wx.ALL,
                           'border': 60}]]
        )



class Block(wx.Panel):
    pass

"""
from rewx import components as c 

[c.block, {},
  ] 


data EntityType 
  = Primitive String
  | Composite 
  | Function 


data EntityType 
  = Primitive wx.Object
  | Composite 
  | Function 


primitives have mount/patch methods 
Composites have life cycles + render/patch 
functions eval to Primitives or Composites


mount :: EntityType -> Parent -> wx.Object 
mount (Primitive x) parent = mount2(x)
mount (Composite x) parent = mount2(x)


def primitive(type): 
    return Primitive(type)

def render(element, parent):
    if isprimitive(element['type']): 
        return mount(element, parent)
    # isclass
    elif type(element['type']) == type:
        return element['type'].Render(element, parent)
    # is sfc 
    elif callable(element['type']):
        # stateless functional component
        return render(element['type'](element['props']), parent)
    else:
        raise Unknown Type 
"""

def render(element, parent):
    if element['type'] == 'statictext':
        return statictext2wx(element, parent)
    elif element['type'] == 'textctrl':
        return textctrl2wx(element, parent)
    elif type(element['type']) == type:
        return element['type'].Render(element, parent)
    elif callable(element['type']):
        # stateless functional component
        return render(element['type'](element['props']), parent)
    else:
        instance: wx.Panel = block2wx(element, parent)
        sizer = instance.GetSizer()
        for child in element['props'].get('children'):
            sizer.Add(
                render(child, instance),
                child['props'].get('proportion', 0),
                child['props'].get('flag', 0),
                child['props'].get('border', 0)
            )
        return instance

def andthen(dom, vdom):
    print('waiting!')
    import time
    time.sleep(2)
    print('running!')
    wx.CallAfter(patch, dom, vdom)


if __name__ == '__main__':
    foo_elm = create_element('block', {}, children=[
        create_element('statictext', {'name': 'Hello', 'value': 'Hey there, world!'}),
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

    foo_elm3 = create_element(Foo, {'item1': 'HELLOOOOO'})
    foo_elm4 = create_element(Bar, {})

    foo_elm5 = create_element(Bar, {'item1': 'HELLOOOOO'})
    foo_elm6 = create_element(Foo, {'item1': 'BYeeeee'})

    # basic_app('My Hello App', foo_elm)
    import wx.lib.inspection
    app = wx.App()
    wx.lib.inspection.InspectionTool().Show()
    frame = wx.Frame(None, title='Test re-wx')
    frame.SetSize((570, 520))
    import wx.adv
    import wx.aui
    from datetime import timedelta
    ai =wx.SpinCtrlDouble(frame,)
    sizer = wx.BoxSizer()
    ai.SetSizer(sizer)
    tc = wx.TextCtrl(ai)
    sizer.Add(tc)
    print('digits:', ai.GetDigits())
    # ai.SetStatusText('Hello World!')

    thing = render(create_element(Clock, {}), frame)
    # thing = patch(thing, foo_elm6)
    # t = Thread(target=andthen, args=(thing, foo_elm6))
    # t.start()
    box = wx.BoxSizer(wx.VERTICAL)
    box.Add(thing, 1, wx.EXPAND)
    box.Add(ai, 0, wx.EXPAND)
    frame.SetSizer(box)
    frame.Show()
    frame.Fit()

    for child in frame.GetChildren():
        for ccc in child.GetChildren():
            for cc in ccc.GetChildren():
                cc.Layout()
            ccc.Layout()
        child.Layout()
    app.MainLoop()


