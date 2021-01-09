import wx
from rewx import create_element, wsx, render
from rewx.components import StaticText, Frame


def say_hello(props):
    return wsx(
        [Frame, {'title': 'My first re-wx app', 'show': True},
         [StaticText, {'label': f'Hello, {props["name"]}!'}]]
    )


if __name__ == '__main__':
    app = wx.App()
    element = create_element(Frame, {'title': 'My Cool Application', 'show': True}, children=[
        create_element(StaticText, {'label': 'Howdy, cool person!'})
    ])
    frame = render(element, None)
    frame.Show()
    app.MainLoop()