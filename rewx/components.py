"""
All components and wrappers currently
supported by rewx.
"""
import wx
import wx.adv


ActivityIndicator = wx.ActivityIndicator
Button = wx.Button
BitmapButton = wx.BitmapButton
CalendarCtrl = wx.adv.CalendarCtrl
CheckBox = wx.CheckBox
CollapsiblePane = wx.CollapsiblePane
ComboBox = wx.ComboBox
Dropdown = ComboBox
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
