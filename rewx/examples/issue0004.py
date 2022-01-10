import wx

from rewx import create_element, wsx, render, Component, Ref
import rewx.components as c


class MyComponent(Component):
    def __init__(self, props):
        super().__init__(props)
        self.state = {'value': ''}
        self.input_ref = Ref()

    def component_did_mount(self):
        wx_ctrl = self.input_ref.instance
        wx_ctrl.Bind(wx.EVT_TEXT_ENTER, self.on_enter)

    def on_input(self, event):
        self.set_state({'value': event.EventObject.Value})

    def on_enter(self, event):
        wx.MessageDialog(None, "Enter pressed!").ShowModal()

    def render(self):
        return wsx(
            [c.Frame, {'title': 'My Cool Application', 'show': True},
             [c.Block, {'orient': wx.HORIZONTAL},
              [c.TextCtrl, {
                  'style': wx.TE_PROCESS_ENTER,
                  'value': self.state['value'],
                  'on_change': self.on_input,
                  'ref': self.input_ref,
              }]]]
        )



if __name__ == '__main__':
    app = wx.App()
    frame = render(create_element(MyComponent, {}), None)
    app.MainLoop()