import wx
from unittest import TestCase

from rewx import create_element, wsx, Component, render
import rewx.components as c

class TestNestedComponents(TestCase):

    def test_update_component(self):
        app = wx.App()
        frame = render(create_element(Parent, {}), None)
        # app.MainLoop()
        # sanity checking that state/props align for initial render
        initial_parent_state = frame._instance.state['label']
        initial_child_props = frame.Children[0]._instance.props['label']
        self.assertEqual(initial_parent_state, initial_child_props)
        # bug #0002 was that child component weren't receiving new props
        # up update. So now we fire one of the rewx handlers:
        frame._instance.update_label('foobar')
        next_parent_state = frame._instance.state['label']
        next_child_props = frame.Children[0]._instance.props['label']
        # and expect that both are still in sync
        self.assertEqual(next_parent_state, 'foobar')
        self.assertEqual(next_parent_state, next_child_props)
        app.Destroy()



class Parent(Component):
    """Test Component"""
    def __init__(self, props):
        super().__init__(props)
        self.state = {
            'label': 'initial'
        }

    def update_label(self, new_value):
        self.set_state({'label': new_value})

    def render(self):
        return wsx([c.Frame, {'show': True},
                    [Nested, {'label': self.state['label']}]])

class Nested(Component):
    """Test Component"""
    def __init__(self, props):
        super().__init__(props)

    def render(self):
        return create_element(c.StaticText, {'label': self.props['label']})