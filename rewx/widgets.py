import wx
import wx.adv
# TODO: warn on unknown props?
# on_click event type needs to be overriden per type
from typing import Union, Optional


def noop(instance, props):
    return instance


def dispatch(func):
    """
    TODO
    """
    registry = {'default': func}

    def register(cls, func=None):
        """TODO"""
        assert issubclass(cls, wx.Object), "TODO! Explain why it must be one of these!"
        if func is None:
            return lambda f: register(cls, f)
        registry[cls] = func
        return func

    def wrapper(element, parent: wx.Window):
        try:
            return registry[element['type']](element, parent)
        except KeyError:
            return registry['default'](element, parent)

    registry[object] = func
    wrapper.register = register
    wrapper.dispatch = dispatch
    return wrapper



"""
basic setters:
```
label -> SetLabel
```

noarg changers:
```
instance.Start()
instance.Stop() 

'start': {
  'true': instance.Start(),
  'false': instance.Stop()
}
```


handlers, which need to know the type of event to bind (which differs based on Instance type): 

on_input -> instance.Bind(wx.EVT_TEXT, handler)
on_input -> instance.Bind(wx.EVT_CHECKBOX, handler) 

on_click -> instance.Bind(wx.EVT_BUTTON, handler)
on_click -> instance.Bind(wx.EVT_LEFT_DOWN, handler)


'on_click': {
    'wx.StaticText': wx.EVT_LEFT_DOWN,
    'wx.Button': wx.EVT_BUTTON,
    ...  
},
'on_change': {
    'wx.StaticText': N/A,
    'wx.Button': N/A,
    'wx.TextCtrl': wx.EVT_TEXT
}

updater :: Instance -> Props -> Instance 

 

"""


basic_controls = {
    '*': {

    },
    'label': 'SetLabel',
    'value': 'SetValue',
    'background_color': 'SetBackgroundColor',
    'foreground_color': 'SetForegroundColour',
    'font': 'SetFont',
    'helptext': 'SetHelpText',
    'name': 'SetName',
    'minsize': 'SetMinSize',
    'maxsize': 'SetMaxSize',
    'tooltip': 'SetToolTip',
    'show': 'Show',
    'style': 'SetStyle',
}


def on_change(instance, props):
    pass


def set_basic_props(instance, props):
    for key, val in props.items():
        if key.startswith('on_'):
            continue
        try:
            getattr(instance, basic_controls[key])(val)
        except KeyError:
            # prop which doesn't apply to this control
            pass
    return instance


@dispatch
def update(instance, props):
    return set_basic_props(instance, props)


def activity_indicator(instance: wx.ActivityIndicator, props: dict):
    set_basic_props(instance, props)
    if props.get('start'):
        instance.Stop()
    else:
        instance.Stop()
    return instance


def calendarctrl(instance: wx.adv.CalendarCtrl, props) -> wx.Object:
    set_basic_props(instance, props)
    additions = {
        'selected_date': 'SetDate',
        'display_holidays': 'EnableHolidayDisplay',
        'allow_month_change': 'EnableMonthChange',
    }
    for prop_key, wx_method in additions.items():
        if prop_key in props:
            getattr(instance, wx_method)(props[prop_key])

    instance.Unbind(wx.adv.EVT_CALENDAR_SEL_CHANGED)
    if props.get('on_change'):
        # TODO: verify callable?
        instance.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, props['on_change'])
    return instance


def checkbox(instance: wx.CheckBox, props):
    set_basic_props(instance, props)
    instance.Unbind(wx.EVT_CHECKBOX)
    if props.get('on_change'):
        instance.Bind(wx.EVT_CHECKBOX, props['on_change'])
    return instance


def collapsiblepanel(instance: wx.CollapsiblePane, props):
    set_basic_props(instance, props)
    instance.Collapse(props.get('collapsed', False))
    instance.Unbind(wx.EVT_COLLAPSIBLEPANE_CHANGED)
    if props.get('on_change'):
        instance.Unbind(wx.EVT_COLLAPSIBLEPANE_CHANGED, props['on_change'])
    return instance



def combobox(instance: wx.ComboBox, props) -> wx.Object:
    set_basic_props(instance, props)
    instance.Clear()
    instance.AppendItems(props.get('choices', []))
    instance.SetValue(props.get('value'))
    # clean up existing handlers (if any)
    instance.Unbind(wx.EVT_COMBOBOX)
    instance.Unbind(wx.EVT_TEXT)
    # rebind as relevant
    if props.get('on_change'):
        instance.Bind(wx.EVT_COMBOBOX, props['on_change'])
    if props.get('on_input'):
        instance.Bind(wx.EVT_TEXT, props['on_input'])
    return instance


def gauge(instance: wx.Gauge, props: dict) -> wx.Object:
    set_basic_props(instance, props)
    if props.get('range'):
        instance.SetRange(props['range'])
    if props.get('pulse', False):
        instance.Pulse()
    return instance


def listbox(instance: wx.ListCtrl, props):
    instance.Un
    return instance




# def checkbox(instance: wx.CheckBox, props: dict):



mapp = {
    'wx.Window': {
        'api': {
            'SetLabel': 'label',
            'SetBackgroundColour': 'background_color',
            'SetForegroundColour': 'foreground_color',
            'SetDropTarget': 'on_drop:lambda',
            'SetFont': 'font: wx.Font',
            'SetHelpText': 'help_text: str',
            'SetName': 'name: str', # very useful for debugging via inspector
            'SetMinSize': 'min_size',
            'SetMaxSize': 'max_size',
            'SetToolTip': 'tooltip',
            'Show': 'show',
            'SetStyle': 'style'
        },
        'wx.ActivityIndicator': {
            'start': 'Start'
        },
        'wx.adv.CalendarCtrl': {
            'selected_date': 'SetDate', # ?
            'holiday_display': 'EnableHolidayDisplay',
            'month_change': 'EnableMonthChange',

            'EVT_CALENDAR_SEL_CHANGED': 'on_change: fn',
        },
        'wx.CheckBox': {
            'SetValue': 'checked: boolean',
            'EVT_CHECKBOX': 'on_change',
            'SetLabel': 'label: str'
        },
        'wx.CollapsiblePanel': {
            'SetCollapsed': 'collapsed: bool',
            'EVT_COLLAPSIBLEPANE_CHANGED': 'on_change'
        },
        'wx.Choice': {

        },
        'wx.ComboBox': {
            'EVT_COMBOBOX': 'on_change',
            'EVT_TEXT': 'on_input',
            'choices': 'choices', # update will use AppendItems
            'SetValue': 'value: str'
        },
        'wx.Gauge': {
            'style': 'style',
            'Pulse': 'pulse: bool',
            'SetRange': 'range: int', # sets the maximum value, so just needs an int
            'SetValue': 'value: int'
        },
        'wx.ListBox': {
            'style': 'style',
            'EVT_LISTBOX': 'on_change',
            'choices': 'choices', # update will use InsertItems,
            'SetSelection': 'value:[str]', # ?
        },
        # this one will be a massive departure from
        # its WX API. See: youtube-dl example for usage
        # TODO: general event escape hatch?
        #       e.g. {'event-handler': {'type': wx.EVT_LIST_COL_CLICK, 'fn': lambda x...}}
        'wx.ListCtrl': {
            'style': 'style',
            'DeleteAllColumns/InsertColumn': 'column_def: [ColumnDef]',
            'DeleteAllItems/SetItem': 'data: [Any]',
            'EVT_LIST_ITEM_SELECTED': 'on_selection', # ?
        },
        'wx.RadioBox': {
            'SetSelection': 'selected: Int',
            'choices': 'choices',
            'EnableItem': 'disabled:[n]',
            'EVT_RADIOBOX': 'on_change'
        },
        'wx.RadioButton': {
            'style': 'FORCE ONLY: wx.RB_SINGLE', # this style is forced so that WX doesn't control the clicky clicky
            'SetValue': 'selected:bool',
            'EVT_RADIOBUTTON': 'on_change'
        },
        # this is just a container like block
        'wx.StaticBox': {
            'label': 'label'
        },
        'wx.Slider': {
            'style': 'style',
            'EVT_SLIDER': 'on_change',
            'SetMax': 'max',
            'SetMin': 'min',
            'SetValue': 'value'
        },
        'wx.SpinCtrl': {
            'style': 'style',
            'EVT_SPINCTRL': 'on_change',
            'SetMax': 'max',
            'SetMin': 'min',
            'SetValue': 'value'
        },
        'wx.SpinCtrlDouble': {
            'style': 'style',
            'EVT_SPINCTRLDOUBLE': 'on_change',
            'SetMax': 'max',
            'SetMin': 'min',
            'SetIncrement': 'increment',
            'SetPrecision': 'precision',
            'SetValue': 'value'
        },
        'wx.StaticBitmap': {
            'SetBitmap': 'uri',
        },
        'wx.Button': {
            'EVT_BUTTON': 'on_click',
            # wx.Control stuff label, enabled, etc..
        },
        'wx.BitmapButton': {
            'EVT_BUTTON': 'on_click',
            'SetBitmap': 'uri'
        },
        'wx.ToggleButton': {
            'EVT_TOGGLEBUTTON': 'on_click',
            'SetValue': 'value:bool'
        },
        'wx.StaticLine': {
            'style': 'style',
        },
        'wx.StatusBar': {
            'SetStatusText': 'text:str'
        },
        'textEntry': {
                'SetEditable',
                'SetHint',
                'ChangeValue' # for updates
            },
    }
}

class MyThing(wx.Panel):
    def __init__(self, *args):
        super().__init__(*args)



import wx



"""
mount :: Type -> Element -> wx.Object 

"""


from functools import singledispatch





@dispatch
def mount(element, parent):
    element['type'](parent)
    print('handling the default case!', element, parent)

@mount.register(wx.Panel)
def foo(element, parent):
    print('handling wx.Panel!')


@mount.register(wx.StaticBitmap)
def foo(element, parent):
    bitmap = wx.Bitmap(element['props']['uri'])
    bitmap._uri = element['props']['uri']
    staticbitmap = wx.StaticBitmap(parent, -1, bitmap)
    return staticbitmap
    print('handling wx.Panel!')


def update_bitmap(instance: wx.StaticBitmap, props):
    if props['uri'] != instance.GetBitmap()._uri:
        bitmap: wx.Bitmap = instance.GetBitmap()
    return instance

@mount.register(wx.Button)
def foo(element, parent):
    print('handling wx.Button!')

mount({'type': wx.TextCtrl}, 'Parent')
mount({'type': wx.Button}, 'Parent')
mount({'type': wx.Panel}, 'Parent')
mount({'type': wx.StaticText}, 'Parent')





import sys
sys.exit(0)




class Managed:
    def mount(self, element, parent: wx.Window) -> wx.Object:
        tc = wx.TextCtrl(parent)
        group = wx.RadioBox(parent, choices=[], style=wx.RB_GROUP)
        return group

    def patch(self, props, instance: wx.Window) -> wx.Object:
        pass



def instantiate_wx(type, element, parent):
    instance = type(parent)
    instance._type = element['type']
    return instance


def assign_props(instance: wx.Panel, props):
    instance.SetToolTip()
    pass

primitives = {
    'statictext': statictext
}

def statictext(element, parent):
    return assign_props(instantiate_wx(wx.StaticText, element, parent), element['props'])


def statictext2wx(element, parent):
    text = wx.StaticText(parent)
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







# OLD BELOW HERE


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