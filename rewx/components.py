"""
All components and wrappers currently
supported by rewx.
"""
import wx
import wx.adv
import wx.lib.scrolledpanel
import wx.richtext
import wx.media
import wx.html
import wx.html2

ActivityIndicator = wx.ActivityIndicator
Button = wx.Button
BitmapButton = wx.BitmapButton
CalendarCtrl = wx.adv.CalendarCtrl
CheckBox = wx.CheckBox
# CollapsiblePane = wx.CollapsiblePane
ComboBox = wx.ComboBox
DirPickerCtrl = wx.DirPickerCtrl
Dropdown = ComboBox
Frame = wx.Frame
Gauge = wx.Gauge
ListBox = wx.ListBox
ListCtrl = wx.ListCtrl
Panel = wx.Panel
RadioBox = wx.RadioBox
RadioButton = wx.RadioButton
Slider = wx.Slider
SpinCtrl = wx.SpinCtrl
SpinCtrlDouble = wx.SpinCtrlDouble
StaticBitmap = wx.StaticBitmap
StaticBox = wx.StaticBox
StaticLine = wx.StaticLine
StaticText = wx.StaticText
TextCtrl = wx.TextCtrl
ToggleButton = wx.ToggleButton
MediaCtrl = wx.media.MediaCtrl
RichTextCtrl = wx.richtext.RichTextCtrl
HtmlWindow = wx.html.HtmlWindow
WebView = wx.html2.WebView
Notebook = wx.Notebook

class Grid(wx.Panel):
    """
    Wrapper type for creating a panel
    with a Grid Sizer
    """
    pass

class FlexGrid(wx.Panel):
    """
    Wrapper type for creating a Panel
    with a FlexGridSizer

    https://wxpython.org/Phoenix/docs/html/wx.FlexGridSizer.html
    """
    pass

class Block(wx.Panel):
    """
    Wrapper type for creating a panel
    with a BoxSizer
    """

class TextArea(wx.TextCtrl):
    """
    TextCtrl Wrapper with it's style pre-baked
    to be TE_MULTILINE
    """
    pass

class SVG(wx.StaticBitmap):
    """
    Wrapper for converting an SVG to a scaled StaticBitmap
    """
    pass

class SVGButton(wx.BitmapButton):
    """
    Wrapper for creating an SVG backed BitmapButton.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NotebookItem(wx.Panel):
    """
    Wrapper allowing the specification of Notebook pages
    as children. e.g.

    ```
    [Notebook, {on_change: handler},
      [NotebookItem, {'active': True}
        [AnyComponent, {...}]],
      [NotebookItem, {'active': False}
        [AnyComponent, {...}]]]
    ```
    """

class FilePickerCtrlOpen(wx.FilePickerCtrl):
    """
    Wrapper for a FilePickerCtrl with default style
    `wx.FLP_OPEN | wx.FLP_FILE_MUST_EXIST`

    https://docs.wxpython.org/wx.FilePickerCtrl.html
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.self_managed = True # creates and destroys its own children

class FilePickerCtrlSave(wx.FilePickerCtrl):
    """
    Wrapper for a `FilePickerCtrl` with style
    `wx.FLP_SAVE`

    https://docs.wxpython.org/wx.FilePickerCtrl.html
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.self_managed = True # creates and destroys its own children

class DirPickerCtrl(wx.DirPickerCtrl):
    """
    Wrapper for a `DirPickerCtrl` with a `FileDropTarget`.

    Extra Props
    ```
    {
      text_font: wx.Font,
      on_change: (event:FileDirPickerEvent),
      on_dropdir: (x:int, y:int, path:str),
    }
    ```
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.self_managed = True # creates and destroys its own children

class ScrolledPanel(wx.lib.scrolledpanel.ScrolledPanel):
    """
    Wrapper for a `ScrolledPanel` which doesn't jump the scroll on focus.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # https://discuss.wxpython.org/t/prevent-scrolledpanel-scrolling-to-a-widget-that-has-focus/27257
    def OnChildFocus(self, event):
        pass
