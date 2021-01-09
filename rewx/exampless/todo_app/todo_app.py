import wx

from rewx import Component, wsx, render, create_element
from rewx import components as c

from util import callwith


def TodoList(props):
    return create_element(c.Block, {}, children=[
        create_element(c.StaticText, {
            'label': f" * {item}",
            'on_click': callwith(props['on_click'], item)})
        for item in props['items']
    ])


class TodoApp(Component):
    def __init__(self, props):
        super().__init__(props)
        self.state = {'items': ['Groceries', 'Laundry'], 'text': ''}

    def handle_change(self, event):
        self.set_state({**self.state, 'text': event.String})

    def handle_submit(self, event):
        self.set_state({
            'text': '',
            'items': [*self.state['items'], self.state['text']]
        })

    def handle_complete(self, event_item):
        self.set_state({
            **self.state,
            'items': [item for item in self.state['items']
                      if item != event_item]
        })

    def render(self):
        return wsx(
            [c.Frame, {'title': 'My TODO app'},
             [c.Block, {'name': 'foooo'},
              [c.StaticText, {'label': 'What needs to be done?'}],
              [c.TextCtrl, {'value': self.state['text'], 'on_change': self.handle_change}],
              [c.Button, {'label': 'Add', 'on_click': self.handle_submit}],
              [c.StaticText, {'label': 'I need to do:'}],
              [TodoList, {'items': self.state['items'], 'on_click': self.handle_complete}]]]
        )


if __name__ == '__main__':
    app = wx.App()
    frame = render(create_element(TodoApp, {}), None)
    frame.Show()
    app.MainLoop()


