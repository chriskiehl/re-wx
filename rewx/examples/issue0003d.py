import wx
from unittest import TestCase

from rewx import create_element, wsx, Component, render
import rewx.components as c

class Parent(Component):
    def __init__(self, props):
        super().__init__(props)
        self.state = {
            'label': 'initial'
        }

    def update_label(self, new_value):
        self.set_state({'label': str(new_value)})

    def render(self):
        return wsx([c.Frame, {'show': True},
                    [Nested, {'label': self.state}],
                    [c.Button, {'label': 'click', 'on_click': self.update_label}]])

class Nested(Component):
    def __init__(self, props):
        super().__init__(props)

    def render(self):
        return create_element(c.StaticText, self.props['label'])

if __name__ == '__main__':
    app = wx.App()
    frame = render(create_element(Parent, {}), None)
    app.MainLoop()