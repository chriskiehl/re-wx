"""
Demoing a simple stateful component which
keeps track of the current time.
"""
import datetime
import wx

from app import basicapp
from rewx.rewx2 import wsx, create_element, Component, Ref
from rewx import components as c

def big_ol_font():
    """
    Creating a nice large font for our clock.

    Note: we create this in a function rather than at the module level
    so that it's invoked at render time. This keeps WX happy, which insists on
    having its wx.App object created before anything else.
    """
    return wx.Font(30, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

class Clock(Component):
    "Clock component"
    def __init__(self, props):
        super().__init__(props)
        self.timer = None
        self.state = {
            'time': datetime.datetime.now()
        }

    def component_did_mount(self):
        self.timer = wx.Timer()
        self.timer.Notify = self.update_clock
        self.timer.Start(milliseconds=1000)

    def update_clock(self):
        self.set_state({'time': datetime.datetime.now()})

    def render(self):
        return wsx(
          [c.Block, {},
           [c.StaticText, {'label': self.state['time'].strftime('%I:%M:%S'),
                           'name': 'ClockFace',
                           'foreground_color': '#51acebff',
                           'font': big_ol_font(),
                           'proporton': 1,
                           'flag': wx.CENTER | wx.ALL,
                           'border': 60}]]
        )


if __name__ == '__main__':
    basicapp(create_element(Clock, {}), title='Clock')


