import threading
import wx
import wx.lib.inspection
from pip._vendor.contextlib2 import contextmanager
from unittest import TestCase

from rewx import create_element, wsx, render
import rewx.components as c


class TestGaugeElement(TestCase):

    def test_gauge(self):
        expected_state = {
            'value': 123,
            'range': 3000,
            'name': 'Counter',
            'size': (500, 30),
        }
        app = wx.App()
        component = wsx(
            [c.Frame, {'show': True, 'size': (999,999)},
             [c.Block, {},
              [c.Gauge, {**expected_state, 'proportion': 0}]]])
        frame = render(component, None)
        gauge = frame.Children[0].Children[0]

        self.assertEqual(gauge.Size, expected_state['size'])
        self.assertEqual(gauge.Range, expected_state['range'])
        self.assertEqual(gauge.Name, expected_state['name'])
        self.assertEqual(gauge.Value, expected_state['value'])



