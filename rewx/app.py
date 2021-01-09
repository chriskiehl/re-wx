import os
import wx.svg
from rewx import render





def basicapp(element,
             title='re-wx application',
             size=(-1, -1),
             debug=False):
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

    dirname = os.path.dirname(__file__)
    frame.SetIcon(wx.Icon(os.path.join(dirname, 'icon.png')))
    frame.SetSize(size)
    if debug:
        import wx.lib.inspection
        wx.lib.inspection.InspectionTool().Show()

    # mbar = wx.MenuBar()
    # frame.SetMenuBar(mbar)
    # menu = wx.Menu()
    # item = wx.MenuItem(menu, wx.ID_NEW, text="Just here for show ^_^", kind=wx.ITEM_NORMAL)
    # menu.Append(item)
    # mbar.Append(menu, 'Media')
    #
    # """
    # [MenuBar, {},
    #   [Menu, {title: 'foobar'},
    #     [MenuItem, {text: "foo"}],
    #     [MenuItem, {text: "Bar"}]],
    #   [Menu, {title: 'Playback'},
    #     [MenuItem, {text: "foo"}],
    #     [MenuItem, {text: "Bar"}]]]]
    # """
    #
    # menu2 = wx.Menu()
    # item2 = wx.MenuItem(
    #     menu,
    #     wx.ID_NEW,
    #     text="Just here for show in v0.0.1 ^_^",
    #     kind=wx.ITEM_NORMAL)
    # menu2.Append(item2)
    # mbar.Append(menu2, 'Playback')





    component = render(element, frame)
    box = wx.BoxSizer(wx.VERTICAL)
    box.Add(component, 1, wx.EXPAND)
    frame.SetSizer(box)
    frame.Show()
    if size == (-1, -1):
        frame.Fit()
    app.MainLoop()

