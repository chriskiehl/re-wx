import os
from rewx import render

dirname = os.path.dirname(__file__)




def basicapp(element, title='re-wx application', debug=False):
    """
    Ultra basic wx.Application shim which renders and attaches
    the supplied element to a top-level frame and then kicks off
    the main wx loop

    Usage:
    ```
    elm = create_element(wx.StaticText, {'label': 'Hello world!'})
    basicapp(elm, title='My App')
    ```
    """
    import wx
    app = wx.App()
    frame = wx.Frame(None, title=title)
    frame.SetIcon(wx.Icon(os.path.join(dirname, 'icon.png')))
    if debug:
        import wx.lib.inspection
        wx.lib.inspection.InspectionTool().Show()
    component = render(element, frame)
    box = wx.BoxSizer(wx.VERTICAL)
    box.Add(component, 1, wx.EXPAND)
    frame.SetSizer(box)
    frame.Show()
    frame.Fit()
    app.MainLoop()

