import wx
import wx.lib.inspection

import sys
from random import randint

import time
from threading import Thread
from uuid import uuid4

import rewx.virtualdom as v
from pyrsistent import pmap, freeze, thaw

from rewx.rewx import Ref
from rewx.rewx import Component, readit22
from wx.lib.pubsub import pub
from rewx.exampless.gooey import components as c
from util import veq

PROGRESS_CHAN = 'PROGRESS_MESSAGES'
DONE_CHAN = 'COMPLETED'

class Screens:
    CONFIG = 'CONFIG'
    RUNNING = 'RUNNING'
    RESULTS = 'RESULTS'


def fake_run():
    time.sleep(1)
    end = time.time() + randint(2, 3)
    while time.time() < end:
        pub.sendMessage(PROGRESS_CHAN, message=f'Countdown: {round(end - time.time(), 2)}s\n')
        time.sleep(0.02)
    pub.sendMessage(PROGRESS_CHAN, message=f'All Done!!\n')
    time.sleep(.5)
    pub.sendMessage(DONE_CHAN, message=f'DONE!')


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
        self.terminal_ref = Ref()
        self.state = freeze({
            'screen': Screens.CONFIG,
            'output': '',
            'options': [{
                'id': str(uuid4()),
                'label': 'Input file',
                'help': 'Path to the input video to convert',
                'required': True,
                'order': 0,
                'value': ''
            }, {
                'id': str(uuid4()),
                'label': 'Output file',
                'help': 'Directory to store the output',
                'required': True,
                'order': 1,
                'value': ''
            }, {
                'id': str(uuid4()),
                'label': 'Frame rate',
                'help': 'Target frame rate to use during encoding',
                'required': False,
                'order': 0,
                'value': ''
            }, {
                'id': str(uuid4()),
                'label': 'Foobar Baz',
                'help': 'Another option I will come up with later',
                'required': False,
                'order': 1,
                'value': ''
            }]
        })
        pub.subscribe(self.log_progress, PROGRESS_CHAN)
        pub.subscribe(self.handle_done, DONE_CHAN)

    def required(self):
        requred = [option for option in self.state.options if option['required']]
        return sorted(requred, key=lambda x: x['order'])

    def optional(self):
        optional = [option for option in self.state.options if not option['required']]
        return sorted(optional, key=lambda x: x['order'])


    def on_edit(self, event):
        """Return to congig screen"""
        self.setState(self.state.set('screen', Screens.CONFIG))

    def on_start(self, event):
        "Start the host program"
        self.setState(self.state.set('screen', Screens.RUNNING))
        thread = Thread(target=fake_run)
        thread.start()

    def on_stop(self, event):
        """Halt the current executing program"""
        self.setState(self.state.set('screen', Screens.RESULTS))
        pass

    def on_close(self, event):
        self.panel_ref.instance.GetParent().Destroy()
        sys.exit(0)

    def handle_input(self, event):
        next_state = self.state.transform(
            ['options', veq('id', event.EventObject.xid)],
            lambda option: option.set('value', event.String))
        self.setState(next_state)

    def log_progress(self, message):
        def update(state):
            return state.set('output', self.state.output + message)
        instance: wx.TextCtrl = self.terminal_ref.instance
        if instance:
            # self.setState(self.state.set('output', self.state.output + message))
            wx.CallAfter(instance.AppendText, message)

    def handle_done(self, message):
        instance: wx.TextCtrl = self.terminal_ref.instance
        self.setState(self.state.set('screen', Screens.RESULTS).set('output', instance.GetValue()))

    def render(self):
        return readit22(
          [v.block22, {'xid': 'main', 'ref': self.panel_ref},
           [c.header, {'title': labels[self.state.screen]['title'],
                       'subtitle': labels[self.state.screen]['subtitle'],
                       'icon_uri': labels[self.state.screen]['icon_uri']}],
           [v.line, {'xid': 'line', 'flag': wx.EXPAND}],

           [c.when, {'is_true': self.state.screen == Screens.CONFIG, 'xid': 'cf'},
            [c.config_page, {'required': self.required(),
                             'optional': self.optional(),
                             'on_change': self.handle_input}],
            [v.line, {'xid': 'line2', 'flag': wx.EXPAND}],
            [c.config_footer, {'on_start': self.on_start, 'on_cancel': self.on_close}]],

           [c.when, {'is_true': self.state.screen == Screens.RUNNING, 'xid': 'rn'},
            [v.textarea, {'xid': 'b', 'value': '',
                          'proportion': 1,
                          'flag': wx.EXPAND | wx.ALL,
                          'border': 20,
                          'readonly': True,
                          'ref': self.terminal_ref}],
            [v.line, {'xid': 'line2', 'flag': wx.EXPAND}],
            [c.runtime_footer, {'on_start': self.on_start, 'on_halt': self.on_stop}]],

           [c.when, {'is_true': self.state.screen == Screens.RESULTS, 'xid': 'rs'},
            [v.textarea, {'xid': 'b', 'value': self.state.output, 'proportion': 1, 'flag': wx.EXPAND | wx.ALL, 'border': 20, 'readonly': True}],
            [v.line, {'xid': 'line2', 'flag': wx.EXPAND}],
            [c.results_footer, {'on_edit': self.on_edit,
                                'on_restart': self.on_start,
                                'on_close': self.on_close}]]]
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