import wx

from components import ActivityIndicator, Block, TextCtrl, Button, BitmapButton
from rewx import create_element, wsx, render
from rewx import components as c


def say_hello(props):
    return wsx(
        [c.Frame, {'title': 'My first re-wx app', 'show': True},
         [c.StaticText, {'label': f'Hello, {props["name"]}!', 'helptext': 'WHAT DOES THIS DO?'}]]
    )

def example(props):
    return wsx(
      [c.Block, {'orient': wx.VERTICAL},
       [c.Block, {'orient': wx.HORIZONTAL, 'flag': wx.EXPAND},
        [c.TextCtrl, {'on_change': props['my_handler']}],
        [c.Button, {'on_click': props['handle_submit']}],
        [c.BitmapButton, {
            'uri': r'C:\Users\Chris\Documents\re-wx\rewx\icon.png',
            # 'background_color': '#ff00ff',
            'min_size': (100, 100),
            'enabled': True}]]]
    )


def foo(*args, **kwags):
    pass

if __name__ == '__main__':
    app = wx.App()
    # element = create_element(Frame, {'title': 'My Cool Application', 'show': True}, children=[
    #     create_element(StaticText, {'label': 'Howdy, cool person!', 'tooltip': 'WHAT DOES THIS DO?'}),
    #     create_element(BitmapButton, {
    #         'uri': r'C:\Users\Chris\Documents\re-wx\rewx\icon.png',
    #         # 'background_color': '#ff00ff',
    #         'min_size': (100,100),
    #         'enabled': True}),
    # ])
    frame = wx.Frame(None)
    comp = render(create_element(example, {'my_handler': foo, 'handle_submit': foo}), frame)
    frame.Show()
    app.MainLoop()