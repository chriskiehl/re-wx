import wx

from components import ActivityIndicator, Block, TextCtrl, Button, BitmapButton
from rewx import create_element, wsx, render
from rewx import components as c


def say_hello(props):
    return wsx(
        [c.Frame, {'title': 'My first re-wx app', 'show': True},
         [c.StaticText, {'label': f'Hello, {props["name"]}!', 'helptext': 'WHAT DOES THIS DO?'}]]
    )


some_data = [
    {'name': 'Timmy',
     'age': 12,
     'occupation': 'Child'},
    {'name': 'Buzz',
     'age': 48,
     'occupation': 'Astronaut'},
    {'name': 'Cloud',
     'age': 28,
     'occupation': 'Avalanche'},
    {'name': 'Spike',
     'age': 27,
     'occupation': 'Bounty Hunter'},
]

def column_defs():
    return [
        {'title': 'NAME', 'column': lambda item: item['name']},
        {'title': 'AGE', 'column': lambda item: str(item['age'])},
        {'title': 'NAME', 'column': lambda item: item['occupation']}]


def example(props):
    return wsx(
      [c.Frame, {'title': 'The Kitchen Sink Demo'},
       [c.Block, {},
        [c.Grid, {'cols': 5},
         [c.TextCtrl, {'on_change': print}],
         [c.Button, {'on_click': print, 'label': 'Click me!'}],
         [c.BitmapButton, {
             'uri': r'C:\Users\Chris\Documents\re-wx\rewx\icon.png',
             'background_color': '#ff00ff',
             'enabled': True}],
         [c.CheckBox, {'value': True, 'label': 'Howdy!', 'on_change': print}],
         [c.ComboBox, {'choices': ['Option One', 'Option Two', 'Option Three'],
                       'value': 'Option One',
                       'on_change': print}]],
        [c.CalendarCtrl, {'on_change': print, 'flag': wx.EXPAND}],
        [c.ListCtrl, {'column_defs': column_defs(),
                      'data': some_data,
                      'flag': wx.EXPAND}],
        [c.Block, {'orient': wx.HORIZONTAL},
        [c.RadioBox, {'choices': ['A', 'B', 'C'],
                      'selected': 1,
                      'on_change': print}],
         [c.StaticBox, {'label': 'My Radio options'},
          [c.Block, {'flag': wx.TOP, 'border': 20},
           [c.RadioButton, {'label': 'A', 'selected': False}],
           [c.RadioButton, {'label': 'B', 'selected': True}],
           [c.RadioButton, {'label': 'C', 'selected': False}],
           [c.RadioButton, {'label': 'D', 'selected': False}]]],
         [c.TextCtrl, {'value': 'Foooobar'}]]]]
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
    frame = render(create_element(example, {}), None)
    # comp = (create_element(example, {'my_handler': foo, 'handle_submit': foo}), frame)
    frame.Show()
    app.MainLoop()