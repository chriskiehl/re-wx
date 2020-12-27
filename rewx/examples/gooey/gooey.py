import wx
import wx.lib.inspection

import sys
from random import randint

import time

import rewx.virtualdom as v
from pyrsistent import pmap, freeze, thaw

from rewx.rewx import Ref
from rewx.rewx import Component, readit22

from rewx.examples.gooey import components as c

class Screens:
    CONFIG = 'CONFIG'
    RUNNING = 'RUNNING'
    RESULTS = 'RESULTS'


def fake_run():
    end = time.time() + randint(3, 6)
    while time.time() < end:
        pass


labels = {
    Screens.CONFIG: {
        'title': 'Gooey re-wx demo',
        'subtitle': 'A visual re-implementation of Gooey using re-wx!',
        'icon_uri': r'C:\Users\Chris\Documents\re-wx\rewx\examples\gooey\images\config_icon.png'
    },
    Screens.RUNNING: {
        'title': 'Running',
        'subtitle': "Just a sec. We're running the program",
        'icon_uri': r'C:\Users\Chris\Documents\re-wx\rewx\examples\gooey\images\running_icon.png'
    },
    Screens.RESULTS: {
        'title': 'Success!',
        'subtitle': 'All done! looks like evertthing ran A-OK',
        'icon_uri': r'C:\Users\Chris\Documents\re-wx\rewx\examples\gooey\images\success_icon.png'
    },
}


class Gooey(Component):
    """
    This is a minimal faked re-implementation of Gooey[0]. It's a
    program that wraps up CLI programs with a nice auto-generated UI.

    This demo is a recreation of its three major screens (config, run, and results)
    to show using rewx to manage complex lifcycles. All of the functionality is
    faked. To see the real program in action, checkout https://github.com/chriskiehl/Gooey!
    """
    def __init__(self):
        super().__init__()
        self.panel_ref = Ref()
        self.state = freeze({
            'screen': Screens.CONFIG,
            'output': '',
        })

    def on_start(self, event):
        "Start the host program"
        self.setState(self.state.set('screen', Screens.RUNNING))

    def on_stop(self):
        """Halt the current executing program"""
        pass

    def on_cancel(self, event):
        self.panel_ref.instance.GetParent().Destroy()
        sys.exit(0)

    def render(self):
        return readit22(
          [v.block22, {'xid': 'main', 'ref': self.panel_ref},
           [c.header, {'title': labels[self.state.screen]['title'],
                       'subtitle': labels[self.state.screen]['subtitle'],
                       'icon_uri': labels[self.state.screen]['icon_uri']}],
           [v.line, {'xid': 'line', 'flag': wx.EXPAND}],
           [c.when, {'is_true': self.state.screen == Screens.CONFIG, 'xid': 'cf'},
            [c.config_page, {}],
            [v.line, {'xid': 'line2', 'flag': wx.EXPAND}],
            [c.config_footer, {'on_start': self.on_start, 'on_cancel': self.on_cancel}]],

           [c.when, {'is_true': self.state.screen == Screens.RUNNING, 'xid': 'rn'},
            [v.text22, {'xid': 'a', 'value': 'RUNNING!!'}],
            [v.line, {'xid': 'line2', 'flag': wx.EXPAND}],
            [c.runtime_footer, {'on_start': self.on_start, 'on_cancel': self.on_cancel}]],
           [c.when, {'is_true': self.state.screen == Screens.RESULTS, 'xid': 'rs'},
            [v.text22, {'xid': 'b', 'value': 'DONE!!!!'}]],
           ]
        )






def app(title, root):
    app = wx.App()
    wx.lib.inspection.InspectionTool().Show()
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


def main():
    homescreen = Gooey()
    app('Youtube-DL', homescreen)

if __name__ == '__main__':
    main()