import wx
from random import random
from typing import Callable
from typing_extensions import TypedDict

from rewx import Component, wsx, create_element, render
import rewx.components as c


class Parent(Component):
    """
    The main 'container' component. It's the root for all
    state management. It passes behaviors down to its children, which
    in turn cause the state here to be modified when fired.
    """
    def __init__(self, props):
        super().__init__(props)
        self.state = {
            'some_value': random()
        }

    def update_value(self, event):
        self.set_state({'some_value': random()})

    def render(self):
        return wsx(
            [c.Frame, {'show': True, 'size': (200, 100)},
             [c.Block, {},
              [c.StaticText, {'label': str(self.state['some_value'])}],
              # checkout the arbitrary prop we've defined here
              [Child, {
                  'click_handler': self.update_value,
                  'label': 'Click me!'
              }]]]
        )


class ChildProps(TypedDict):
    """Optionally typing the props of your component"""
    label: str
    click_handler: Callable[[wx.CommandEvent], None]


class Child(Component):
    """
    An arbitrary component. Note that this is still pure -- it holds
    no state of its own and all behaviors, like the click handler, are
    passed in via props.
    """
    def __init__(self, props: ChildProps):
        super().__init__(props)

    def render(self):
        return wsx([c.Button, {
            'on_click': self.props['click_handler'],
            'label': self.props['label']
        }])

if __name__ == '__main__':
    app = wx.App()
    frame = render(create_element(Parent, {}), None)
    app.MainLoop()