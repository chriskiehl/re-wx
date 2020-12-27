import wx


class MyForm(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Key Press Tutorial 2")

        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        sizer = wx.BoxSizer(wx.VERTICAL)

        btn = self.onWidgetSetup(wx.Button(panel, label="OK"),
                                 wx.EVT_KEY_UP,
                                 self.onButtonKeyEvent, sizer)
        txt = self.onWidgetSetup(wx.TextCtrl(panel, value=""),
                                 wx.EVT_KEY_DOWN, self.onTextKeyEvent,
                                 sizer)
        panel.SetSizer(sizer)

    def onWidgetSetup(self, widget, event, handler, sizer):
        widget.Bind(event, handler)
        sizer.Add(widget, 0, wx.ALL, 5)
        return widget

    def onButtonKeyEvent(self, event):
        keycode = event.GetKeyCode()
        print(keycode)
        if keycode == wx.WXK_SPACE:
            print("you pressed the spacebar!")
        event.Skip()

    def onTextKeyEvent(self, event):
        keycode = event.GetKeyCode()
        print(keycode)
        if keycode == wx.WXK_DELETE:
            print("you pressed the delete key!")
        event.Skip()


# Run the program
if __name__ == "__main__":
    app = wx.App()
    frame = MyForm()
    frame.Show()
    app.MainLoop()