import wx
from unittest import TestCase

from rewx import create_element, wsx, render
from rewx.components import Gauge, Frame


class TestGaugeElement(TestCase):

    def test_gauge(self):
        expected_state = {
            'value': 123,
            'range': 3000,
            'name': 'Counter',
            'size': (500, 1),
        }
        app = wx.App()
        component = wsx([Frame, {'show': True}, [Gauge, expected_state]])
        frame = render(component, None)
        gauge = frame.Children[0]

        self.assertEqual(gauge.Size, expected_state['size'])
        self.assertEqual(gauge.Range, expected_state['range'])
        self.assertEqual(gauge.Name, expected_state['name'])
        self.assertEqual(gauge.Value, expected_state['value'])


