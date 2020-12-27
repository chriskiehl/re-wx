import wx
import wx.lib.inspection
import rewx.virtualdom as v
from pyrsistent import pmap, freeze, thaw

from rewx.rewx import Component, readit22

from rewx.examples.gooey import components as c

class Screens:
    CONFIG = 'CONFIG'
    RUNNING = 'RUNNING'
    FINAL = 'FINAL'



class Gooey(Component):

    def __init__(self):
        super().__init__()
        self.state = freeze({
            'screen': Screens.CONFIG,
            'required': [{}],
            'optional': [{}],
            'widgets': [{
                'id': 1,
                'type': 'DirChooser',
                'value': ''
            },{
                'id': 2,
                'type': 'FileChooser',
                'value': ''
            }, {
                'id': 3,
                'type': 'TextInput',
                'value': ''
            }]
        })

    def on_start(self, event):
        pass

    def on_cancel(self, event):
        pass

    def render(self):
        if self.state.screen == Screens.CONFIG:
            return readit22(
              [v.block22, {'xid': 'main'},
               [c.header, {'title': 'Gooey re-wx demo',
                           'subtitle': 'A visual re-implementation of Gooey using re-wx!',
                           'icon_uri': r'C:\Users\Chris\Documents\re-wx\rewx\examples\gooey\images\config_icon.png'}],
               [v.line, {'xid': 'line', 'flag': wx.EXPAND}],
               [c.config_page, {}],
               [v.line, {'xid': 'line', 'flag': wx.EXPAND}],
               [c.config_footer, {'on_start': self.on_start, 'on_cancel': self.on_cancel}]]
            )
        elif self.state.screen == Screens.RUNNING:
            return readit22(
              [c.runtime_footer, {'on_start': self.on_start, 'on_cancel': self.on_cancel}]
            )
        else:
            return readit22(
              [c.finished_footer, {}]
            )






def app(title, root):
    app = wx.App()
    wx.lib.inspection.InspectionTool().Show()
    frame = wx.Frame(None, title='Test re-wx')
    frame.SetSize((530, 300))
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


def main():
    homescreen = Gooey()
    app('Youtube-DL', homescreen)

if __name__ == '__main__':
    main()