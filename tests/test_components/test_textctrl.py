import wx
import wx.lib.inspection
from unittest import TestCase
from unittest.mock import MagicMock

from rewx import create_element, wsx, render
import rewx.components as c


class TestTextCtrlElement(TestCase):

    def test_textctrl(self):
        mocked_change_handler = MagicMock()
        mocked_enter_handler = MagicMock()
        expected_state = {
            'value': '123',
            'name': 'My Cool Control',
            'style': wx.TE_PROCESS_ENTER,
            'on_change': mocked_change_handler,
            'size': (100, 20)
        }

        app = wx.App()
        component = wsx(
            [c.Frame, {'show': True, 'size': (999, 999)},
             # note: the inner block is required so that the widget's
             # size prop can be honored (without it, it'd get resized to
             # the parent frame's size after `Layout` gets called.
             [c.Block, {},
              [c.TextCtrl, {**expected_state, 'proportion': 0}]]])
        frame = render(component, None)
        instance = frame.Children[0].Children[0]


        try:
            instance.Bind(wx.EVT_TEXT_ENTER, mocked_enter_handler)
        except Exception:
            self.fail("""
                Unexpected failure. 
                Either the test definition has regressed, and it is now missing 
                `wx.TE_PROCESS_ENTER` as a style argument, or the widget dispatcher 
                has regressed and is no longer applying `style` props correctly""")

        # our props are honored
        self.assertEqual(instance.Name, expected_state['name'])
        self.assertEqual(instance.Value, expected_state['value'])
        self.assertEqual(instance.Size, expected_state['size'])

        # our enter has picked up and installed
        self.assertFalse(mocked_enter_handler.called)
        event = wx.KeyEvent(wx.wxEVT_TEXT_ENTER)
        instance.ProcessEvent(event)
        self.assertTrue(mocked_enter_handler.called)

        # our change handler prop is honored
        self.assertFalse(mocked_change_handler.called)
        event = wx.CommandEvent(wx.wxEVT_TEXT, wx.Window.NewControlId())
        event.SetString('a')
        instance.ProcessEvent(event)
        self.assertTrue(mocked_change_handler.called)

