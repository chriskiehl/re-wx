"""
This module contains all of the mount/update
functions for re-wx's supported widget types.
"""
from operator import attrgetter
import wx
import wx.adv
import wx.media
import wx.html
import wx.html2
import wx.svg
# TODO: warn on unknown props?
import os
import weakref
from rewx.dispatch import mount, update
from wx.richtext import RichTextCtrl
import sys
from rewx.components import Block, Grid, FlexGrid, TextArea, SVG, SVGButton, NotebookItem, FilePickerCtrlOpen, FilePickerCtrlSave, DirPickerCtrl, ScrolledPanel
from rewx.util import exclude
from rewx.bitmap_support import load, resize_image, to_bitmap
from rewx.util import identity

dirname = os.path.dirname(__file__)

def noop(*args, **kwargs):
    return None


basic_controls = {
    '*': {
    },
    'label': 'SetLabel',
    'value': 'SetValue',
    'background_color': 'SetBackgroundColour',
    'foreground_color': 'SetForegroundColour',
    'font': 'SetFont',
    'helptext': 'SetHelpText',
    'name': 'SetName',
    'min_size': 'SetMinSize',
    'max_size': 'SetMaxSize',
    'tooltip': 'SetToolTip',
    'show': 'Show',
    'enabled': 'Enable',
    'style': 'SetStyle',
    'wx_name': 'SetName'
}

exclusions = {
    wx.ActivityIndicator: {'value', 'label'},
    wx.ListBox: {'value', 'label'},
    wx.Button: {'value', 'style'},
    wx.StaticLine: {'value', 'style'},
    wx.Gauge: {'value'},
    wx.BitmapButton: {'value'},
    wx.adv.CalendarCtrl: {'value'},
    wx.Frame: {'value'},
    Block: {'style'},
    SVG: {'value'},
    SVGButton: {'value'},
    ScrolledPanel: {'value'},
    DirPickerCtrl: {'value', 'style'},
    FilePickerCtrlOpen: {'value', 'style'},
    FilePickerCtrlSave: {'value', 'style'},
    FlexGrid: {'value', 'label', 'style'},
    wx.StaticBitmap: {'value'},
    wx.ToggleButton: {'value'},
    wx.ComboBox: {'style'},
}




def set_basic_props(instance, props):
    available_controls = exclude(basic_controls, exclusions.get(instance.__class__, []))
    for key, val in props.items():
        if key.startswith('on_'):
            continue
        if key in available_controls:
            setter_name = available_controls[key]
            if hasattr(instance, setter_name):
                getattr(instance, setter_name)(val)
    return instance


@mount.register(wx.Frame)
def frame(element, parent) -> wx.Frame:
    instance = wx.Frame(None)
    props = element['props']
    if 'size' in props:
        instance.SetSize(props['size'])
    instance.SetDoubleBuffered(props.get('double_buffered', False))
    return update(element, instance)


@update.register(wx.Frame)
def frame(element, instance: wx.Frame):
    props = element['props']
    set_basic_props(instance, props)
    if 'title' in props:
        instance.SetTitle(props['title'])
    if 'show' in props:
        instance.Show(props['show'])
    if 'icon_uri' in props:
        icon = wx.Icon(props['icon_uri'])
        instance.SetIcon(icon)
        if sys.platform != 'win32':
            # OSX needs to have its taskbar icon explicitly set
            # bizarrely, wx requires the TaskBarIcon to be attached to the Frame
            # as instance data (self.). Otherwise, it will not render correctly.
            frame.taskbarIcon = wx.adv.TaskBarIcon(iconType=wx.adv.TBI_DOCK)
            frame.taskbarIcon.SetIcon(icon)
    else:
        instance.SetIcon(wx.Icon(os.path.join(dirname, 'icon.png')))
    if 'on_close' in props:
        instance.Bind(wx.EVT_CLOSE, props['on_close'])

    return instance


@mount.register(wx.ActivityIndicator)
def activity_indicator(element, parent):
    return update(element, wx.ActivityIndicator(parent))

@update.register(wx.ActivityIndicator)
def activity_indicator(element, instance: wx.ActivityIndicator):
    props = element['props']
    set_basic_props(instance, props)
    if props.get('start'):
        instance.Start()
    else:
        instance.Stop()
    return instance

@mount.register(wx.Button)
def button(element, parent):
    return update(element, wx.Button(parent, style=element['props'].get('style', 0)))


@update.register(wx.Button)
def button(element, instance: wx.Button):
    props = element['props']
    set_basic_props(instance, props)
    # Removed this behavior because I don't want it, and it causes a problem
    # because the Button grabs focus on every render when disabled.
    #
    # if props.get('enabled') is False:
    #     # we navigate away from the control when disabling.
    #     # Without this, under conditions where the button gets
    #     # disabled / re-enabled quickly, wx will still feed events
    #     # spawned while it was disable to the now recently enabled
    #     # button. This behavior doesn't happen if we navigate away
    #     instance.Navigate()
    if 'label_markup' in props:
        instance.SetLabelMarkup(props['label_markup'])
    instance.Unbind(wx.EVT_BUTTON)
    if props.get('on_click'):
        instance.Bind(wx.EVT_BUTTON, props['on_click'])
    return instance


@mount.register(wx.ToggleButton)
def togglebutton(element, parent):
    return update(element, wx.ToggleButton(parent))


@update.register(wx.ToggleButton)
def togglebutton(element, instance: wx.ToggleButton):
    props = element['props']
    set_basic_props(instance, props)
    instance.Unbind(wx.EVT_TOGGLEBUTTON)
    if props.get('on_click'):
        instance.Bind(wx.EVT_TOGGLEBUTTON, props['on_click'])
    return instance



@mount.register(wx.BitmapButton)
def bitmapbutton(element, parent):
    return update(element, wx.BitmapButton(parent))


@update.register(wx.BitmapButton)
def bitmapbutton(element, instance: wx.BitmapButton):
    props = element['props']
    set_basic_props(instance, props)

    if instance.GetBitmap():
        instance.GetBitmap().Destroy()
    if 'uri' in props:
        bitmap = wx.Bitmap(props.get('uri'))
        instance.SetBitmap(bitmap)

    instance.Unbind(wx.EVT_BUTTON)
    if props.get('on_click'):
        instance.Bind(wx.EVT_BUTTON, props['on_click'])
    return instance


@mount.register(wx.adv.CalendarCtrl)
def calendarctrl(element, parent):
    return update(element, wx.adv.CalendarCtrl(parent))


@update.register(wx.adv.CalendarCtrl)
def calendarctrl(element, instance: wx.adv.CalendarCtrl) -> wx.Object:
    props = element['props']
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

@mount.register(wx.CheckBox)
def checkbox(element, parent):
    return update(element, wx.CheckBox(parent))


@update.register(wx.CheckBox)
def checkbox(element, instance: wx.CheckBox):
    props = element['props']
    set_basic_props(instance, props)
    instance.Unbind(wx.EVT_CHECKBOX)
    if props.get('on_change'):
        instance.Bind(wx.EVT_CHECKBOX, props['on_change'])
    return instance

# TODO: this requires special care
# to handle children additions / removals
@mount.register(wx.CollapsiblePane)
def collapsiblepanel(element, parent):
    return update(element, wx.CollapsiblePane(parent))

@update.register(wx.CollapsiblePane)
def collapsiblepanel(element, instance: wx.CollapsiblePane):
    props = element['props']
    set_basic_props(instance, props)
    instance.Collapse(props.get('collapsed', False))
    instance.Unbind(wx.EVT_COLLAPSIBLEPANE_CHANGED)
    if props.get('on_change'):
        instance.Unbind(wx.EVT_COLLAPSIBLEPANE_CHANGED, props['on_change'])
    return instance


@mount.register(wx.ComboBox)
def combobox(element, parent):
    props = element['props']
    return update(
        element,
        wx.ComboBox(parent, choices=props.get('choices', []), style=props.get('style', 0))
        )

@update.register(wx.ComboBox)
def combobox(element, instance: wx.ComboBox) -> wx.Object:
    props = exclude(element['props'], {'value'})
    # ComboBox is a textctrl and listbox linked together.
    # Updating one causes events to fire for the other, so
    # to avoid doubling up the events, we unhook everything,
    # perform the updates, and then re-add the handlers.
    instance.Unbind(wx.EVT_COMBOBOX)
    instance.Unbind(wx.EVT_TEXT)

    set_basic_props(instance, props)
    # we blanket delete/recreate the items for now, which
    # seems to be Good Enough. Child diffing could be benchmarked
    # to see if it's worth the effort.
    for _ in instance.GetItems():
        instance.Delete(0)
    instance.AppendItems(props.get('choices', []))
    if 'value' in element['props']:
        instance.SetSelection(props['choices'].index(element['props'].get('value')))

    if props.get('on_change'):
        instance.Bind(wx.EVT_COMBOBOX, props['on_change'])
    if props.get('on_input'):
        instance.Bind(wx.EVT_TEXT, props['on_input'])

    return instance

class DirPickerDropTarget(wx.FileDropTarget):
    """
    We are required to inherit from wx.FileDropTarget
    """
    def __init__(self, dirPickerCtrl, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dirPickerCtrl = dirPickerCtrl 
    def OnDropFiles(self, x:int, y:int, filenames:list[str]):
        if len(filenames) == 1:
            path = filenames[0]
            if os.path.isdir(path):
                dpc = self.dirPickerCtrl()
                if dpc is not None:
                    if hasattr(dpc, '_on_change'):
                        dpc._on_change(path)
                        return True # wx.DragCopy?
        return False # wx.DragNone?
    def OnDragOver(self, x:int, y:int, defResult):
        return wx.DragCopy

@mount.register(DirPickerCtrl)
def dir_picker_ctrl(element, parent):
    instance = DirPickerCtrl(parent)
    # TODO We only need this droptarget in Microsoft Windows.
    # In Linux this is handled automatically.
    # https://docs.wxpython.org/wx.FileDropTarget.html
    instance.droptarget = DirPickerDropTarget(weakref.ref(instance))
    instance.SetDropTarget(instance.droptarget)
    return update(element, instance)

@update.register(DirPickerCtrl)
def dir_picker_ctrl(element, instance: DirPickerCtrl):
    props = element['props']
    set_basic_props(instance, props)
    if instance.HasTextCtrl():
        textctrl = instance.GetTextCtrl()
        if 'text_font' in props:
            textctrl.SetFont(props['text_font'])
    additions = {
        'path': 'SetPath'
    }
    for prop_key, wx_method in additions.items():
        if prop_key in props:
            getattr(instance, wx_method)(props[prop_key])
    instance.Unbind(wx.EVT_DIRPICKER_CHANGED)
    if 'on_change' in props:
        instance._on_change = props['on_change']
        instance.Bind(wx.EVT_DIRPICKER_CHANGED, instance._on_change_impl)
    else:
        if hasattr(instance, '_on_change'):
            delattr(instance, '_on_change')
    return instance

@mount.register(FilePickerCtrlOpen)
def file_picker_ctrl_open(element, parent):
    return update(element, FilePickerCtrlOpen(parent))

@update.register(FilePickerCtrlOpen)
def file_picker_ctrl_open(element, instance: FilePickerCtrlOpen):
    props = element['props']
    set_basic_props(instance, props)
    additions = {
        'path': 'SetPath'
    }
    for prop_key, wx_method in additions.items():
        if prop_key in props:
            getattr(instance, wx_method)(props[prop_key])
    instance.Unbind(wx.EVT_FILEPICKER_CHANGED)
    if props.get('on_change'):
        instance.Bind(wx.EVT_FILEPICKER_CHANGED, props['on_change'])
    return instance

@mount.register(FilePickerCtrlSave)
def file_picker_ctrl_save(element, parent):
    props = element['props']
    return update(element, FilePickerCtrlSave(parent, style=wx.FLP_SAVE, wildcard=props.get('wildcard', '*.*')))

@update.register(FilePickerCtrlSave)
def file_picker_ctrl_save(element, instance: FilePickerCtrlSave):
    props = element['props']
    set_basic_props(instance, props)
    additions = {
        'path': 'SetPath'
    }
    for prop_key, wx_method in additions.items():
        if prop_key in props:
            getattr(instance, wx_method)(props[prop_key])
    instance.Unbind(wx.EVT_FILEPICKER_CHANGED)
    if props.get('on_change'):
        instance.Bind(wx.EVT_FILEPICKER_CHANGED, props['on_change'])
    return instance

@mount.register(wx.Gauge)
def gauge(element, parent):
    size = element['props'].get('size', (-1, -1))
    gauge = wx.Gauge(parent, size=size)
    gauge._pulsing = False
    return update(element, gauge)

@update.register(wx.Gauge)
def gauge(element, instance: wx.Gauge) -> wx.Object:
    props = element['props']
    if 'range' in props:
        instance.SetRange(props['range'])
    if 'value' in props:
        value = props['value']
        if value < 0:
            instance.Pulse()
            instance._pulsing = True
        else:
            instance._pulsing = False
            value = min(int(value), instance.GetRange())
            if instance.GetValue() != value:
                # Windows 7 progress bar animation hack:
                # http://stackoverflow.com/questions/5332616/disabling-net-progressbar-animation-when-changing-value
                # tl;dr: set it to the desired range then subtract 1.
                if props.get('disable_animation', False) and sys.platform.startswith("win"):
                    if instance.GetRange() == value:
                        instance.SetValue(value)
                        instance.SetValue(value - 1)
                    else:
                        instance.SetValue(value + 1)
                else:
                    instance.SetValue(value)
    set_basic_props(instance, props)
    return instance


@mount.register(wx.ListBox)
def listbox(element, parent):
    return update(element, wx.ListBox(parent, choices=element['props'].get('choices', [])))

@update.register(wx.ListBox)
def listbox(element, instance: wx.ListBox):
    props = element['props']
    # ComboBox is a textctrl and listbox linked together.
    # Updating one causes events to fire for the other, so
    # to avoid doubling up the events, we unhook everything,
    # perform the updates, and then re-add the handlers.
    # instance.Unbind(wx.EVT_LISTBOX)

    set_basic_props(instance, props)
    # we blanket delete/recreate the items for now, which
    # seems to be Good Enough. Child diffing could be benchmarked
    # to see if it's worth the effort.
    if set(instance.GetItems()) != set(props.get('choices', [])):
        for _ in instance.GetItems():
            instance.Delete(0)
        instance.AppendItems(props.get('choices', []))

    if 'value' in props:
        instance.SetSelection(element['props'].get('value'))

    # TODO: control this component similar to Notebook
    if props.get('on_change'):
        instance.Unbind(wx.EVT_LISTBOX)
        instance.Bind(wx.EVT_LISTBOX, props['on_change'])

    return instance


@mount.register(wx.ListCtrl)
def listctrl(element, parent):
    instance = wx.ListCtrl(parent, style=wx.LC_REPORT)
    instance.self_managed = True
    return update(element, instance)

@update.register(wx.ListCtrl)
def listctrl(element, instance: wx.ListCtrl):
    props = {**element['props']}
    if 'style' in props:
        del props['style']
    set_basic_props(instance, props)
    # TODO: what events...?
    restored_widths = ListCtrl_GetColumnWidths(instance)
    instance.DeleteAllColumns()
    instance.DeleteAllItems()
    for e, col in enumerate(props.get('column_defs', [])):
        instance.InsertColumn(e, col['title'])
    ListCtrl_SetColumnWidths(instance, restored_widths)

    for row_idx, item in enumerate(props.get('data', [])):
        instance.InsertItem(row_idx, '')
        for col_idx, coldef in enumerate(props.get('column_defs', [])):
            instance.SetItem(row_idx, col_idx, coldef['column'](item))
    return instance

def ListCtrl_GetColumnWidths(instance: wx.ListCtrl):
    wds = []
    for i in range(0, instance.GetColumnCount()):
        wds.append(instance.GetColumnWidth(i))
    return wds

def ListCtrl_SetColumnWidths(instance: wx.ListCtrl, wds: list[int]): # : List[int]):
    # no-op if the list of column widths is the wrong length
    if len(wds) == instance.GetColumnCount():
        for i in range(0, len(wds)):
            instance.SetColumnWidth(i, wds[i])



@mount.register(wx.media.MediaCtrl)
def mediactrl(element, parent):
    return update(element, wx.media.MediaCtrl(parent,
                                              style=wx.SIMPLE_BORDER))

@update.register(wx.media.MediaCtrl)
def mediactrl(element, instance: wx.media.MediaCtrl):
    # TODO: fixme
    props = element['props']
    instance.SetMinSize((300,300))
    # set_basic_props(instance, props)
    if 'on_load' in props:
        instance.Bind(wx.media.EVT_MEDIA_LOADED, props['on_load'])
    # if
    # if props.get('start'):
    #     instance.Stop()
    # else:
    #     instance.Stop()
    return instance



@mount.register(SVG)
def svg(element, parent):
    return update(element, SVG(parent))

@update.register(SVG)
def svg(element, instance: SVG) -> SVG:
    props = element['props']
    set_basic_props(instance, props)
    if props.get('uri'):
        if getattr(instance, '_rewx_uri', None) != props.get('uri') \
                or tuple(instance.GetBitmap().GetSize()) != props.get('size'):
            svg = wx.svg.SVGimage.CreateFromFile(element['props']['uri'])
            size = wx.Size(*props.get('size', (svg.width, svg.height)))
            bitmap = svg.ConvertToScaledBitmap(size)
            instance.SetBitmap(bitmap)
            instance._rewx_uri = props['uri']
            return instance
        else:
            # everything is samezies
            return instance
    else:
        # URI isn't present, so we replace the current bitmap (if
        # any) with a blank one
        instance.SetBitmap(wx.Bitmap())
        return instance


@mount.register(SVGButton)
def svgbutton(element, parent):
    return update(element, SVGButton(parent))

@update.register(SVGButton)
def svgbutton(element, instance: SVGButton) -> SVGButton:
    props = element['props']
    set_basic_props(instance, props)

    instance.Unbind(wx.EVT_BUTTON)
    if props.get('on_click'):
        instance.Bind(wx.EVT_BUTTON, props['on_click'])

    set_basic_props(instance, props)
    if props.get('uri'):
        if getattr(instance, '_rewx_uri', None) != props.get('uri') \
                or tuple(instance.GetBitmap().GetSize()) != props.get('size'):
            svg = wx.svg.SVGimage.CreateFromFile(element['props']['uri'])
            size = wx.Size(*props.get('size', (svg.width, svg.height)))
            bitmap = svg.ConvertToScaledBitmap(size)
            instance.SetBitmap(bitmap)
            instance._rewx_uri = props['uri']
            return instance
        else:
            # everything is samezies
            return instance
    else:
        # URI isn't present, so we replace the current bitmap (if
        # any) with a blank one
        instance.SetBitmap(wx.Bitmap())
        return instance



@mount.register(wx.RadioBox)
def radiobox(element, parent):
    return update(element, wx.RadioBox(parent))

@update.register(wx.RadioBox)
def radiobox(element, instance: wx.RadioBox):
    """
    Note: choices are not possible to change after
    being created when using RadioBox. Thus, they're
    not modified here.
    """
    props = element['props']
    set_basic_props(instance, props)
    if props.get('selected'):
        instance.SetSelection(props['selected'])
    instance.Unbind(wx.EVT_RADIOBOX)
    if props.get('on_change'):
        instance.Bind(wx.EVT_RADIOBOX, props['on_change'])


@mount.register(wx.StaticBox)
def staticbox(element, parent):
    instance = wx.StaticBox(parent)
    sizer = wx.BoxSizer(element['props'].get('orient', wx.VERTICAL))
    instance.SetSizer(sizer)
    return update(element, instance)

@update.register(wx.StaticBox)
def staticbox(element, instance: wx.StaticBox):
    props = element['props']
    # TODO: does this auto-use a sizer..?
    set_basic_props(instance, props)

    return instance

@mount.register(wx.Slider)
def slider(element, parent):
    return update(element, wx.Slider(parent))

@update.register(wx.Slider)
def slider(element, instance: wx.Slider):
    props = element['props']
    set_basic_props(instance, props)
    instance.SetMax(props.get('max', 100))
    instance.SetMin(props.get('min', 0))
    instance.Unbind(wx.EVT_SLIDER)
    if 'on_change' in props:
        instance.Bind(wx.EVT_SLIDER, props['on_change'])
    return instance


@mount.register(wx.SpinCtrl)
def spinctrl(element, parent):
    return update(element, wx.SpinCtrl(parent))

@update.register(wx.SpinCtrl)
def spinctrl(element, instance: wx.SpinCtrl):
    props = element['props']
    set_basic_props(instance, props)
    instance.SetMax(props.get('max', 100))
    instance.SetMin(props.get('min', 0))
    instance.Unbind(wx.EVT_SPINCTRL)
    if 'on_change' in props:
        instance.Bind(wx.EVT_SPINCTRL, props['on_change'])
    return instance


@mount.register(wx.SpinCtrlDouble)
def spinctrldouble(element, parent):
    instance = wx.SpinCtrlDouble(parent)
    instance.self_managed = True # SpinCtrlDouble has a self-managed child.
    return update(element, instance)

@update.register(wx.SpinCtrlDouble)
def spinctrldouble(element, instance: wx.SpinCtrlDouble):
    props = element['props']
    set_basic_props(instance, props)
    instance.SetMax(props.get('max', 100))
    instance.SetMin(props.get('min', 0))
    instance.SetIncrement(props.get('increment', 0))
    if 'digits' in props:
        instance.SetDigits(props['digits'])
    instance.Unbind(wx.EVT_SPINCTRLDOUBLE)
    if 'on_change' in props:
        instance.Bind(wx.EVT_SPINCTRLDOUBLE, props['on_change'])
    return instance


@mount.register(wx.StaticText)
def statictext(element, parent):
    return update(element, wx.StaticText(parent))

@update.register(wx.StaticText)
def statictext(element, instance: wx.StaticText):
    # TODO: it does NOT response to 'SetValue'
    # this means set_basic needs to accept a map, not use
    # a fixed list.
    props = element['props']
    set_basic_props(instance, props)
    instance.Unbind(wx.EVT_LEFT_DOWN)
    if 'on_click' in props:
        instance.Bind(wx.EVT_LEFT_DOWN, props['on_click'])
    return instance

@mount.register(wx.html2.WebView)
def webview(element, parent):
    return update(element, wx.html2.WebView.New(parent))


@update.register(wx.html2.WebView)
def webview(element, instance: wx.html2.WebView):
    # TODO: it does NOT response to 'SetValue'
    # this means set_basic needs to accept a map, not use
    # a fixed list.
    props = {**element['props']}
    value = props.get('value','')
    if 'value' in props:
        instance.SetPage(props['value'], '/')
    return instance


@mount.register(wx.html.HtmlWindow)
def htmlwindow(element, parent):
    return update(element, wx.html.HtmlWindow(parent))


@update.register(wx.html.HtmlWindow)
def htmlwindow(element, instance: wx.html.HtmlWindow):
    # TODO: it does NOT response to 'SetValue'
    # this means set_basic needs to accept a map, not use
    # a fixed list.
    props = {**element['props']}
    value = props.get('value','')
    if 'value' in props:
        instance.SetPage(props['value'])
    return instance



@mount.register(RichTextCtrl)
def richtextctrl(element, parent):
    setonce_styles = element['props'].get('style', wx.TE_MULTILINE)
    return update(element, RichTextCtrl(parent, style=setonce_styles | wx.TE_MULTILINE))


@update.register(RichTextCtrl)
def richtextctrl(element, instance: RichTextCtrl):
    # TODO: it does NOT response to 'SetValue'
    # this means set_basic needs to accept a map, not use
    # a fixed list.
    props = {**element['props']}
    value = props.get('value','')
    if 'value' in props:
        del props['value']
    # The style argument has different meaning at construction
    # time versus instance time. At construction, it's the usual
    # wx style flags. However, once the instance is created, 'style'
    # controls the internal style of the textctrl's text buffer
    if 'style' in props:
        del props['style']

    set_basic_props(instance, props)
    before = instance.GetInsertionPoint()
    instance.ChangeValue(value)
    instance.SetInsertionPoint(before)
    instance.Unbind(wx.EVT_LEFT_DOWN)
    instance.Unbind(wx.EVT_TEXT)
    if 'on_click' in props:
        instance.Bind(wx.EVT_LEFT_DOWN, props['on_click'])
    if 'on_change' in props:
        instance.Bind(wx.EVT_TEXT, props['on_change'])
    return instance


@mount.register(TextArea)
def textarea(element, parent):
    setonce_styles = element['props'].get('style', wx.TE_MULTILINE)
    return update(element, TextArea(parent, style=setonce_styles | wx.TE_MULTILINE))

@update.register(TextArea)
def textarea(element, instance: TextArea):
    # TODO: it does NOT response to 'SetValue'
    # this means set_basic needs to accept a map, not use
    # a fixed list.
    props = {**element['props']}
    value = props.get('value','')
    if 'value' in props:
        del props['value']
    # The style argument has different meaning are construction
    # time versus instance time. At construction, it's the usual
    # wx style flags. However, once the instance is created, 'style'
    # controls the internal style of the textctrl's text buffer
    if 'style' in props:
        del props['style']

    set_basic_props(instance, props)
    before = instance.GetInsertionPoint()
    instance.ChangeValue(value)
    instance.SetInsertionPoint(before)
    instance.Unbind(wx.EVT_LEFT_DOWN)
    instance.Unbind(wx.EVT_TEXT)
    if 'on_click' in props:
        instance.Bind(wx.EVT_LEFT_DOWN, props['on_click'])
    if 'on_change' in props:
        instance.Bind(wx.EVT_TEXT, props['on_change'])
    return instance



@mount.register(wx.Panel)
def panel(element, parent):
    return update(element, wx.Panel(parent))


@update.register(wx.Panel)
def panel(element, instance: wx.Panel):
    props = element['props']
    set_basic_props(instance, props)
    instance.Unbind(wx.EVT_LEFT_DOWN)
    if 'on_click' in props:
        instance.Bind(wx.EVT_LEFT_DOWN, props['on_click'])
    return instance


@mount.register(Block)
def block(element, parent):
    panel = update(element, Block(parent, style=element['props'].get('style', wx.TAB_TRAVERSAL)))
    sizer = wx.BoxSizer(element['props'].get('orient', wx.VERTICAL))
    panel.SetSizer(sizer)
    return panel

@update.register(Block)
def block(element, instance: Block):
    props = element['props']
    set_basic_props(instance, props)
    instance.Unbind(wx.EVT_LEFT_DOWN)
    if 'on_click' in props:
        instance.Bind(wx.EVT_LEFT_DOWN, props['on_click'])
    instance.Unbind(wx.EVT_SIZE)
    if 'on_size' in props:
        instance.Bind(wx.EVT_SIZE, props['on_size'])
    return instance



@mount.register(ScrolledPanel)
def scrolledpanel(element, parent):
    panel = update(element, ScrolledPanel(parent))
    sizer = wx.BoxSizer(element['props'].get('orient', wx.VERTICAL))
    panel.SetSizer(sizer)
    return panel

@update.register(ScrolledPanel)
def scrolledpanel(element, instance: ScrolledPanel):
    props = element['props']
    set_basic_props(instance, props)
    # Only call SetupScrolling if the props changed.
    # https://docs.wxpython.org/wx.lib.scrolledpanel.ScrolledPanel.html#wx.lib.scrolledpanel.ScrolledPanel.SetupScrolling
    # https://github.com/wxWidgets/Phoenix/blob/de0a4415c05e7483b2960c6dc9720154269244a8/wx/lib/scrolledpanel.py#L120
    scroll_x = props.get('scroll_x', False)
    scroll_y = props.get('scroll_y', False)
    rate_x = props.get('rate_x', 20)
    rate_y = props.get('rate_y', 20)
    if (not hasattr(instance, 'last_scroll_x')
        or instance.last_scroll_x != scroll_x
        or not hasattr(instance, 'last_scroll_y')
        or instance.last_scroll_y != scroll_y
        or not hasattr(instance, 'last_rate_x')
        or instance.last_rate_x != rate_x
        or not hasattr(instance, 'last_rate_y')
        or instance.last_rate_y != rate_y
        ):
        instance.SetupScrolling(
            scroll_x=scroll_x,
            scroll_y=scroll_y,
            rate_x=rate_x,
            rate_y=rate_y
        )
    instance.last_scroll_x = scroll_x
    instance.last_scroll_y = scroll_y
    instance.last_rate_x = rate_x
    instance.last_rate_y = rate_y
    instance.Unbind(wx.EVT_LEFT_DOWN)
    if 'on_click' in props:
        instance.Bind(wx.EVT_LEFT_DOWN, props['on_click'])
    instance.Unbind(wx.EVT_SIZE)
    if 'on_size' in props:
        instance.Bind(wx.EVT_SIZE, props['on_size'])
    instance.Unbind(wx.EVT_MOTION)
    if 'on_mouse_motion' in props:
        instance.Bind(wx.EVT_MOTION, props['on_mouse_motion'])
    instance.Unbind(wx.EVT_MOUSEWHEEL)
    if 'on_mouse_wheel' in props:
        instance.Bind(wx.EVT_MOUSEWHEEL, props['on_mouse_wheel'])
    instance.Unbind(wx.EVT_SCROLLWIN)
    if 'on_scrollwin' in props:
        instance.Bind(wx.EVT_SCROLLWIN, props['on_scrollwin'])
    return instance



@mount.register(Grid)
def grid(element, parent):
    props = element['props']
    panel = Grid(parent)
    sizer = wx.GridSizer(props.get('cols', 1), gap=props.get('gap', (0, 0)))
    panel.SetSizer(sizer)
    return update(element, panel)

@update.register(Grid)
def grid(element, instance: Grid):
    props = element['props']
    set_basic_props(instance, props)
    instance.Unbind(wx.EVT_LEFT_DOWN)
    if 'on_click' in props:
        instance.Bind(wx.EVT_LEFT_DOWN, props['on_click'])
    return instance


@mount.register(FlexGrid)
def flexgrid(element, parent):
    props = element['props']
    panel = FlexGrid(parent)
    sizer = wx.FlexGridSizer(props.get('cols', 1), gap=props.get('gap', (0, 0)))
    panel.SetSizer(sizer)
    return update(element, panel)

@update.register(FlexGrid)
def flexgrid(element, instance: FlexGrid):
    props = element['props']
    set_basic_props(instance, props)
    instance.Unbind(wx.EVT_LEFT_DOWN)
    if 'on_click' in props:
        instance.Bind(wx.EVT_LEFT_DOWN, props['on_click'])
    return instance


@mount.register(wx.TextCtrl)
def textctrl(element, parent):
    style = element['props'].get('style', wx.TE_LEFT)
    size = element['props'].get('size', (-1, -1))
    return update(element, wx.TextCtrl(parent, style=style, size=size))


@update.register(wx.TextCtrl)
def textctrl(element, instance: wx.TextCtrl):
    props = {**element['props']}
    if 'style' in props:
        del props['style']

    value = props.get('value')
    try:
        del props['value']
    except KeyError:
        pass
    set_basic_props(instance, props)
    if 'editable' in props:
        instance.SetEditable(props['editable'])
    if value is not None:
        instance.ChangeValue(value)
    instance.Unbind(wx.EVT_TEXT)
    if 'on_change' in props:
        instance.Bind(wx.EVT_TEXT, props['on_change'])
    instance.Unbind(wx.EVT_SET_FOCUS)
    if 'on_focus_set' in props:
        instance.Bind(wx.EVT_SET_FOCUS, props['on_focus_set'])
    instance.Unbind(wx.EVT_KILL_FOCUS)
    if 'on_focus_kill' in props:
        instance.Bind(wx.EVT_KILL_FOCUS, props['on_focus_kill'])
    return instance


@mount.register(wx.StaticBitmap)
def staticbitmap(element, parent):
    instance = wx.StaticBitmap(parent)
    instance._rewx_cache = {}
    if element['props'].get('uri'):
        uri = element['props'].get('uri')
        instance._rewx_cache['uri'] = uri
        bitmap = wx.Bitmap(uri)
        instance.SetBitmap(bitmap)
    return update(element, instance)


@update.register(wx.StaticBitmap)
def staticbitmap(element, instance: wx.StaticBitmap):
    props = element['props']
    set_basic_props(instance, props)
    if props.get('uri'):
        # only load and update the image if it has changed.
        if instance._rewx_cache.get('uri', 'rewx::nothing') != props['uri']:
            if instance.GetBitmap():
                instance.GetBitmap().Destroy()
            bitmap = wx.Bitmap(props.get('uri'))
            instance.SetBitmap(bitmap)
            instance._rewx_cache['uri'] = props.get('uri')

        # ditto: only resize the image if its size prop has actually changed
        if 'size' in props and props['size'] != instance.GetSize():
            bitmap = to_bitmap(resize_image(load(props['uri']), props['size']))
            instance.SetBitmap(bitmap)
    if 'on_click' in props:
        instance.Bind(wx.EVT_LEFT_DOWN, props['on_click'])
    return instance


@mount.register(wx.StaticLine)
def staticline(element, parent):
    style = element['props'].get('style', wx.HORIZONTAL)
    return update(element, wx.StaticLine(parent, style))


@update.register(wx.StaticLine)
def staticline(element, instance: wx.StaticLine):
    set_basic_props(instance, element['props'])
    return instance


@mount.register(wx.RadioBox)
def radiobox(element, parent):
    return update(element, wx.RadioBox(parent, choices=element['props'].get('choices', [])))


@update.register(wx.RadioBox)
def radiobox(element, instance: wx.RadioBox):
    props = element['props']
    set_basic_props(instance, props)
    if 'selected' in props:
        instance.SetSelection(props['selected'])
    if 'enabled_items' in props:
        for item in props['enabled_items']:
            instance.EnableItem(item)
    instance.Unbind(wx.EVT_RADIOBOX)
    if 'on_change' in props:
        instance.Bind(wx.EVT_RADIOBOX, props['on_change'])
    return instance


@mount.register(wx.RadioButton)
def radiobutton(element, parent):
    # we force the style RB_SINGLE here and don't
    # allow it to be overriden so that these individual
    # buttons can act as controlled components
    return update(element, wx.RadioButton(parent, style=wx.RB_SINGLE))


@update.register(wx.RadioButton)
def radiobutton(element, instance: wx.RadioButton):
    # TODO: exclude style prop
    props = element['props']
    set_basic_props(instance, props)
    instance.SetValue(props.get('selected', False))
    instance.Unbind(wx.EVT_RADIOBUTTON)
    if 'on_change' in props:
        instance.Bind(wx.EVT_RADIOBUTTON, props['on_change'])
    return instance


def notebook_selection(f):
    def inner(event):
        # we want the state to drive the component, not the
        # other way around. So, we clobber any incoming changes
        # and defer to the user's handler.
        event.GetEventObject().ChangeSelection(event.OldSelection)
        return f(event)
    return inner

@mount.register(wx.Notebook)
def notebook(element, parent):
    instance = wx.Notebook(parent, element['props'].get('style', wx.BK_DEFAULT))
    instance._changeHandler = None
    return update(element, instance)

@update.register(wx.Notebook)
def notebook(element, instance: wx.Notebook):
    props = element['props']
    set_basic_props(instance, props)
    # handler = notebook_selection(props.get('on_change', identity))
    # if instance._changeHandler != handler:
    instance.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, props.get('on_change', identity))
        # instance._changeHandler = handler
    return instance



@mount.register(NotebookItem)
def notebookitem(element, parent):
    instance = NotebookItem(parent)
    parent: wx.Notebook = instance.GetParent()
    if not isinstance(parent, wx.Notebook):
        raise Exception('Notebook items can only be used with Notebooks')
    parent.AddPage(instance, element['props'].get('title', 'Tab #XXX'))
    sizer = wx.BoxSizer(element['props'].get('orient', wx.VERTICAL))
    instance.SetSizer(sizer)
    return update(element, instance)


@update.register(NotebookItem)
def notebookitem(element, instance: NotebookItem):
    if element['props'].get('selected', False):
        parent = instance.GetParent()
        for index, child in enumerate(parent.GetChildren()):
            if child == instance:
                parent.ChangeSelection(index)
                parent.Layout()
                break
    # set_basic_props(instance, element['props'])
    return instance


# TODO: keeping this arond to eventually generate prop validation
_supported_props = {
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
        'wx.Listbox': {
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



