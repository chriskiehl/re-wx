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
Dropdown = ComboBox
Frame = wx.Frame
Gauge = wx.Gauge
ListBox = wx.ListBox
ListCtrl = wx.ListCtrl
Panel = wx.Panel
RadioBox = wx.RadioBox
RadioButton = wx.RadioButton
ScrolledPanel = wx.lib.scrolledpanel.ScrolledPanel
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
