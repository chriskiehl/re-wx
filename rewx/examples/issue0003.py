import threading
import time
import wx
from concurrent.futures import ThreadPoolExecutor
from random import randint
from typing import Tuple, Callable, Any

from components import StaticText
from rewx import Component, wsx, render, create_element
from rewx.components import Block, Button, Gauge


def fake_download(args: Tuple[str, Callable[[Any], None]]):
    id, update_fn = args
    # pick an arbitrary amount of seconds for the "download" to take
    duration = randint(3, 7)
    # just to make it more visually exciting, we chunk each second
    # into 10 sub-steps
    duration_steps = duration * 10
    step_size = 100 / duration_steps

    for i in range(duration_steps+1):
        time.sleep(0.01)
        # CallAfter is used to safely send an action to the
        # main WX Thread
        wx.CallAfter(update_fn, item={
            'id': id,
            'percent': step_size * i,
            'status': 'Downloading',
            'eta': duration,
        })
    # Gauge's display lags behind its actual value because of
    # how it animates. So, we give a final sleep here after
    # completing our fake work just so that gauge's animation has
    # time to catch back up.
    time.sleep(1)



class FooGauge(Component):
    def __init__(self, props):
        super().__init__(props)
        self.props = props
        self.state = {
            "download_1": 0,
            "download_2": 0,
            # in practice, these downloads would be stored in
            # a proper data structure. They're stored flatly here
            # just for example.
            'status': 'READY'
        }

    def finish_download(self):
        wx.MessageDialog(None, "Download complete!", 'Alert').ShowModal()
        self.set_state({**self.state, 'status': 'READY'})

    def start_download(self, event):
        self.set_state({**self.state, "status": 'DOWNLOADING'})
        thread = threading.Thread(target=self.start_fake_downloads)
        thread.start()

    def update_downloads(self, item):
        self.set_state({
            **self.state,
            item['id']: item['percent']
        })

    def start_fake_downloads(self):
        with ThreadPoolExecutor() as executor:
            args = [
                ('download_1', self.update_downloads),
                ('download_2', self.update_downloads)]
            results = list(executor.map(fake_download, args))
            wx.CallAfter(self.finish_download)


    def render(self):
        return wsx(
            [Block, {},
             [Block, {'orient': wx.HORIZONTAL},
              [StaticText, {'label': 'Download #1'}],
              [Gauge, {"value": self.state["download_1"],
                       "range": 100}]],
             [Block, {'orient': wx.HORIZONTAL},
              [StaticText, {'label': 'Download #2'}],
              [Gauge, {"value": self.state["download_2"],
                       "range": 100}]],
             [Button, {"label": "Download" if self.state['status'] == 'READY' else 'In Progress',
                       'enabled': self.state['status'] == 'READY',
                       "on_click": self.start_download,
                       "flag": wx.CENTER | wx.ALL}],
            ]
        )


if __name__ == "__main__":
    app = wx.App()

    frame = wx.Frame(None, title="Gauge With Update")
    body = render(create_element(FooGauge, {}), frame)

    frame.Show()
    app.MainLoop()