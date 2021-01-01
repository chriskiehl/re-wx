import threading
import wx
from wx.lib.scrolledpanel import ScrolledPanel

def basic_app(title, root):
    app = wx.App()
    # wx.lib.inspection.InspectionTool().Show()
    frame = wx.Frame(None, title='Test re-wx')
    frame.SetSize((570, 520))
    box = wx.BoxSizer(wx.VERTICAL)
    box.Add(root(frame), 1, wx.EXPAND)
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


def readit22(schema):
    if not schema:
        return None
    if isinstance(schema, dict):
        # TODO: uhh... does this logic hold..?
        # this has already been transformed
        return schema
    fn, *args = schema
    if getattr(fn, '__name__', '') in ('text22', 'input22', 'button22', 'textctrl', 'statictext'):
        return fn(*args)
    else:
        attr, *body = args
        return fn(attr, *map(readit22, body))

class Ref:
    def __init__(self):
        self.instance = None

    def update_ref(self, instance):
        self.instance = instance


class Component:
    def __init__(self):
        self._instance = None
        self.state = None
        self.props = {}

    def setState(self, nextState):
        #todo: this lock does nothing.. needs to be am update fn fr cas
        with threading.Lock():
            # compare and swap the states
            # reconsile changes
            # notify componentDidUpdate
            self.state = nextState
            wx.CallAfter(updater, self._instance, self.render())
            # nextPlainData = self.render()
            # self.mount(nextPlainData)

    def setState2(self, fn):
        with threading.Lock():
            self.state = fn(self.state)
            wx.CallAfter(updater, self._instance, self.render())

    def render(self):
        pass

    def update(self, elm):
        pass

    def component_did_mount(self):
        pass

    def __call__(self, parent):
        if self._instance is None:
            factory = renderer(self.render())
            instance = factory(parent)
            self.component_did_mount()
            self._instance = instance
            return instance
        else:
            raise ValueError('I cannot even right now')


# TODO: componentDidMount
# TODO: componentDidUpdate
# TODO: need React.fragment style component!

def updater(prevdom: wx.Window, newdom):
    """
    Tree structure the same:
        update all in place by id
    Tree structure different:
        find where it diverges
        delete and recreate
    """
    if not any([getattr(x, 'xid', None) for x in prevdom.GetChildren()]):
        missing_xid = 10
    if prevdom.xid != newdom['attrs']['xid']:
        parent = prevdom.GetParent()
        parent.Freeze()
        thunk = renderer(newdom)
        prevdom.Destroy()
        # connect it to the instance
        thunk(parent)
        parent.Layout()
        parent.Thaw()
        for child in parent.GetChildren():
            for ccc in child.GetChildren():
                for cc in ccc.GetChildren():
                    cc.Layout()
                    cc.Refresh()
                ccc.Layout()
                ccc.Refresh()
            child.Layout()
            child.Refresh()
    elif [x.xid for x in prevdom.GetChildren()] != [x['attrs']['xid'] for x in newdom['children']]:
        parent = prevdom.GetParent()
        parent.Freeze()

        for child in prevdom.GetChildren():
            prevdom.RemoveChild(child)
            child.Destroy()
        for i in range(len(prevdom.GetSizer().GetChildren())):
            prevdom.GetSizer().Remove(0)
        for child in newdom['children']:
            thunk = renderer(child)
            item = thunk(prevdom)
            prevdom.GetSizer().Add(item,
                                   child['attrs'].get('proportion', 0),
                                   child['attrs'].get('flag', 0),
                                   child['attrs'].get('border', 0)
                                   )
        # connect it to the instance
        # node: wx.Window = thunk(parent)
        parent.Layout()
        parent.Thaw()
        # node.Show(False)
        # node.Show(True)
        for child in parent.GetChildren():
            for ccc in child.GetChildren():
                for cc in ccc.GetChildren():
                    cc.Layout()
                    cc.Refresh()
                ccc.Layout()
                ccc.Refresh()
            child.Layout()
            child.Refresh()
    else:
        # sync this component + each of its children
        parent = prevdom.GetParent()
        parent.Freeze()
        if newdom['type'] == 'statictext':
            updatestatictext(prevdom, newdom)
        elif newdom['type'] == 'textctrl':
            updatetextctrl(prevdom, newdom)
        elif newdom['type'] == 'textarea':
            updatetextarea(prevdom, newdom)
        elif newdom['type'] == 'listctrl':
            updatelistctrl(prevdom, newdom)
        elif newdom['type'] == 'bitmapbtn':
            updatebitmapbtn(prevdom, newdom)
        elif newdom['type'] == 'gauge':
            updategauge(prevdom, newdom)
        for prevChild, nextChild in zip(prevdom.GetChildren(), newdom['children']):
            updater(prevChild, nextChild)
        parent.Thaw()



def updatestatictext(instance: wx.StaticText, elm):
    instance.SetLabel(elm['attrs']['value'])
    if elm['attrs'].get('disabled', False):
        instance.Disable()
    else:
        instance.Enable()
    instance.Unbind(wx.EVT_LEFT_DOWN)
    if 'on_click' in elm['attrs']:
        instance.Bind(wx.EVT_LEFT_DOWN, elm['attrs']['on_click'])

def updatetextctrl(instance: wx.TextCtrl, elm):
    before = instance.GetInsertionPoint()
    instance.ChangeValue(elm['attrs']['value'])
    instance.SetInsertionPoint(before)
    if elm['attrs'].get('disabled', False):
        instance.Disable()
    else:
        instance.Enable()
    if 'on_change' in elm['attrs']:
        instance.Unbind(wx.EVT_TEXT)
        instance.Bind(wx.EVT_TEXT, elm['attrs']['on_change'])

def updatetextarea(instance: wx.TextCtrl, elm):
    before = instance.GetInsertionPoint()
    instance.ChangeValue(elm['attrs']['value'])
    instance.SetInsertionPoint(before)
    if elm['attrs'].get('disabled', False):
        instance.Disable()
    else:
        instance.Enable()
    if 'on_change' in elm['attrs']:
        instance.Unbind(wx.EVT_TEXT)
        instance.Bind(wx.EVT_TEXT, elm['attrs']['on_change'])


def updatebitmapbtn(instance: wx.BitmapButton, elm):
    bitmap = wx.Bitmap(elm['attrs']['uri'])
    instance.SetBitmap(bitmap)
    if elm['attrs'].get('disabled', False):
        instance.Disable()
    else:
        instance.Enable()
    if 'on_click' in elm['attrs']:
        instance.Unbind(wx.EVT_TEXT)
        instance.Bind(wx.EVT_TEXT, elm['attrs']['on_click'])


def updatelistctrl(instance: wx.ListCtrl, elm):
    # TODO: smarter updates
    # if instance.GetColumnCount() == len(elm['attrs'].get('cols')):
    #     for e, col in enumerate(elm['attrs'].get('cols')):
    #         instance.Set
    # else:

    if elm['attrs'].get('disabled', False):
        instance.Disable()
    else:
        instance.Enable()

    instance.DeleteAllColumns()
    instance.DeleteAllItems()
    for e, col in enumerate(elm['attrs'].get('cols')):
        instance.InsertColumn(e, col['title'])

    for row_idx, item in enumerate(elm['attrs']['data']):
        instance.InsertItem(row_idx, '')
        for col_idx, coldef in enumerate(elm['attrs'].get('cols')):
            instance.SetItem(row_idx, col_idx, str(coldef['column'](item)))
    return instance


def renderer(spec):
    """
    :: Spec -> (Parent -> wxWidget)
    """
    if not spec:
        return None
    if spec['type'] in ('statictext',):
        return statictext2wx(spec)
    elif spec['type'] in ('textctrl',):
        return textctrl2wx(spec)
    elif spec['type'] in ('textarea',):
        return textarea2wx(spec)
    elif spec['type'] in ('button',):
        return button2wx(spec)
    elif spec['type'] in ('dropdown',):
        return dropdown2wx(spec)
    elif spec['type'] in ('listctrl',):
        return listctrl2wx(spec)
    elif spec['type'] in ('bitmap',):
        return bitmap2wx(spec)
    elif spec['type'] in ('bitmapbtn',):
        return bitmapbutton2wx(spec)
    elif spec['type'] in ('gauge',):
        return guage2wx(spec)
    elif spec['type'] in ('scrolledblock',):
        return scrollblock2wx(spec)
    elif spec['type'] in ('vblock',):
        return vblock2wx(spec)
    elif spec['type'] in ('staticline',):
        return line2wx(spec)
    elif spec['type'] in ('grid',):
        return grid2wx(spec)
    else:
        return block2wx(spec)


def block2wx(spec):
    def inner(parent):
        panel = wx.Panel(parent)
        if 'ref' in spec['attrs']:
            ref = spec['attrs']['ref']
            ref.update_ref(panel)
        panel.xid = spec['attrs']['xid']
        if 'min_size' in spec['attrs']:
            panel.SetMinSize(spec['attrs']['min_size'])
        if 'max_size' in spec['attrs']:
            panel.SetMaxSize(spec['attrs']['max_size'])
        if 'background_color' in spec['attrs']:
            panel.SetBackgroundColour(spec['attrs']['background_color'])
        box = wx.BoxSizer((spec.get('attrs') or {}).get('dir', wx.VERTICAL))
        for elm in spec['children']:
            ee = renderer(elm)
            e = ee(panel)
            box.Add(e, elm['attrs'].get('proportion', 0),
                    elm['attrs'].get('flag', 0),
                    elm['attrs'].get('border', 0))
        panel.SetSizer(box)
        return panel
    inner.__tt__ = 'div'
    return inner

def vblock2wx(spec):
    def inner(parent):
        panel = wx.Panel(parent)
        panel.xid = spec['attrs']['xid']
        if 'min_size' in spec['attrs']:
            panel.SetMinSize(spec['attrs']['min_size'])
        if 'max_size' in spec['attrs']:
            panel.SetMaxSize(spec['attrs']['max_size'])
        if 'background_color' in spec['attrs']:
            panel.SetBackgroundColour(spec['attrs']['background_color'])
        box = wx.BoxSizer((spec.get('attrs') or {}).get('dir', wx.VERTICAL))
        box.AddStretchSpacer(1)
        for elm in spec['children']:
            ee = renderer(elm)
            e = ee(panel)
            box.Add(e,
                    elm['attrs'].get('proportion', 0),
                    elm['attrs'].get('flag', 0),
                    elm['attrs'].get('border', 0))
        box.AddStretchSpacer(1)
        panel.SetSizer(box)
        return panel
    return inner

def grid2wx(spec):
    def inner(parent):
        panel = wx.Panel(parent)
        panel.xid = spec['attrs']['xid']
        if 'min_size' in spec['attrs']:
            panel.SetMinSize(spec['attrs']['min_size'])
        if 'max_size' in spec['attrs']:
            panel.SetMaxSize(spec['attrs']['max_size'])
        if 'background_color' in spec['attrs']:
            panel.SetBackgroundColour(spec['attrs']['background_color'])
        box = wx.GridSizer(spec['attrs'].get('cols', 1), gap=spec['attrs'].get('gap', (0, 0)))
        for elm in spec['children']:
            ee = renderer(elm)
            e = ee(panel)
            box.Add(e,
                    elm['attrs'].get('proportion', 0),
                    elm['attrs'].get('flag', 0),
                    elm['attrs'].get('border', 0))
        panel.SetSizer(box)
        return panel
    inner.__tt__ = 'div'
    return inner


def scrollblock2wx(spec):
    def inner(parent):
        panel = ScrolledPanel(parent)
        panel.SetupScrolling(scroll_x=False, scrollToTop=False)
        panel.xid = spec['attrs']['xid']
        box = wx.BoxSizer((spec.get('attrs') or {}).get('dir', wx.VERTICAL))
        for elm in spec['children']:
            ee = renderer(elm)
            e = ee(panel)
            box.Add(e,
                    elm['attrs'].get('proportion', 0),
                    elm['attrs'].get('flag', 0),
                    elm['attrs'].get('border', 0))
        panel.SetSizer(box)
        return panel
    return inner



def line2wx(spec):
    def inner(parent):
        line = wx.StaticLine(parent, style=spec['attrs'].get('style', wx.LI_HORIZONTAL))
        line.SetSize(spec['attrs'].get('size', (10, 10)))
        line.xid = spec['attrs']['xid']
        return line
    return inner


def statictext2wx(spec):
    def inner(parent):
        text = wx.StaticText(parent)
        text.SetLabel(spec['attrs'].get('value'))
        text.xid = spec['attrs']['xid']
        if spec['attrs'].get('font'):
            text.SetFont(spec['attrs']['font'])
        if spec['attrs'].get('on_click'):
            text.Bind(wx.EVT_LEFT_DOWN, spec['attrs'].get('on_click'))
        return text
    return inner


def textctrl2wx(spec):
    def wrapper(f):
        def inner(event):
            return f(event)
        return inner

    def inner(parent):
        text = wx.TextCtrl(parent)
        if spec['attrs'].get('disabled', False):
            text.Disable()
        if 'ref' in spec['attrs']:
            ref = spec['attrs']['ref']
            ref.update_ref(text)
        text.SetValue(spec['attrs'].get('value', ''))
        text.xid = spec['attrs']['xid']
        text.SetEditable(not spec['attrs'].get('readonly', False))
        if spec['attrs'].get('on_change'):
            text.Bind(wx.EVT_TEXT, wrapper(spec['attrs']['on_change']))
        return text
    return inner


def textarea2wx(spec):
    def wrapper(f):
        def inner(event):
            return f(event)
        return inner

    def inner(parent):
        text = wx.TextCtrl(parent, style=wx.TE_MULTILINE)
        text.SetValue(spec['attrs'].get('value'))
        text.xid = spec['attrs']['xid']
        if 'ref' in spec['attrs']:
            ref = spec['attrs']['ref']
            ref.update_ref(text)
        if spec['attrs'].get('disabled', False):
            text.Disable()
        if spec['attrs'].get('on_change'):
            text.Bind(wx.EVT_TEXT, wrapper(spec['attrs']['on_change']))
        return text
    return inner

def bitmap2wx(spec):
    def wrapper(f):
        def inner(event):
            return f(event)
        return inner

    def inner(parent):
        bitmap = wx.Bitmap(spec['attrs']['uri'])
        bitmap.xid = spec['attrs'].get('xid')
        staticbitmap = wx.StaticBitmap(parent, -1, bitmap)
        staticbitmap.xid = spec['attrs'].get('xid')
        return staticbitmap
        # bitmapbutton = wx.BitmapButton(parent, -1, bitmap)
        # # if spec['attrs'].get('selected'):
        # #     dropdown.SetValue(spec['attrs'].get('selected'))
        # # if spec['attrs'].get('on_change'):
        # #     dropdown.Bind(wx.EVT_COMBOBOX, wrapper(spec['attrs']['on_change']))
        # bitmapbutton.xid = spec['attrs'].get('xid')
        # return bitmapbutton
    return inner


def updategauge(instance: wx.Gauge, elm):
    instance.xid = elm['attrs']['xid']
    if elm['attrs'].get('range'):
        instance.SetRange(elm['attrs'].get('range'))
    if elm['attrs'].get('value'):
        instance.SetValue(elm['attrs'].get('value'))
    if elm['attrs'].get('pulse'):
        instance.Pulse()


def guage2wx(spec):
    def wrapper(f):
        def inner(event):
            return f(event)
        return inner

    def inner(parent):
        gauge = wx.Gauge(parent)
        updategauge(gauge, spec)
        return gauge
    return inner


def bitmapbutton2wx(spec):
    def wrapper(f):
        def inner(event):
            return f(event)
        return inner

    def inner(parent):
        bitmap = wx.Bitmap(spec['attrs']['uri'])
        bitmapbutton = wx.BitmapButton(parent, -1, bitmap)
        if spec['attrs'].get('disabled', False):
            bitmapbutton.Disable()
        else:
            bitmapbutton.Enable()
        if spec['attrs'].get('on_click'):
            bitmapbutton.Bind(wx.EVT_BUTTON, wrapper(spec['attrs']['on_click']))
        bitmapbutton.xid = spec['attrs'].get('xid')
        return bitmapbutton
    return inner


def dropdown2wx(spec):
    def wrapper(f):
        def inner(event):
            return f(event)
        return inner

    def inner(parent):
        dropdown = wx.ComboBox(parent, choices=spec['attrs'].get('choices', []))
        # dropdown.AppendItems()
        dropdown.xid = spec['attrs']['xid']
        if spec['attrs'].get('selected'):
            dropdown.SetValue(spec['attrs'].get('selected'))
        if spec['attrs'].get('on_change'):
            dropdown.Bind(wx.EVT_COMBOBOX, wrapper(spec['attrs']['on_change']))
        return dropdown
    return inner


def listctrl2wx(spec):
    def inner(parent):
        listctrl = wx.ListView(parent, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        listctrl.xid = spec['attrs']['xid']
        for e, col in enumerate(spec['attrs'].get('cols')):
            listctrl.InsertColumn(e, col['title'])

        for row_idx, item in enumerate(spec['attrs']['data']):
            listctrl.InsertItem(row_idx, '')
            for col_idx, coldef in enumerate(spec['attrs'].get('cols')):
                listctrl.SetItem(row_idx, col_idx, coldef['column'](item))
        return listctrl
    return inner


def button2wx(spec):
    def wrapper(f):
        def inner(event):
            return f(event)
        return inner

    def inner(parent):
        text = wx.Button(parent, label=spec['attrs'].get('label', ''))
        text.xid = spec['attrs']['xid']
        if spec['attrs'].get('on_click'):
            text.Bind(wx.EVT_BUTTON, wrapper(spec['attrs']['on_click']))
        return text
    return inner

