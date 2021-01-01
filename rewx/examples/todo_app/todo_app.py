from rewx.rewx import Component, wsx


def TodoList(props):
    """
    Stateless functional component
    """
    return wsx(
        ['block', {},
         *[['statictext', {'label': f" * {item['text']}"}]
           for item in props['items']]]
    )

class TodoApp(Component):
    """
    APP DOCS TODO
    """
    def __init__(self, props):
        super().__init__(props)
        self.state = {
            'items': [],
            'text': ''
        }

    def handle_change(self, event):
        self.set_state({**self.state, 'text': event.String})

    def handle_submit(self, event):
        if not self.state['text'].strip():
            return
        else:
            self.set_state({
                'text': '',
                'items': [*self.state['items'], self.state['text']]
        })

    def render(self):
        return wsx(
            ['block', {},
             [TodoList, {'items': self.state['items']}],
             ['statictext', {'label': 'What needs to be done?'}],
             ['textctrl', {'value': self.state['text'], 'on_change': self.handle_change}],
             ['button', {'label': 'Add', 'on_click': self.handle_submit}]]
        )


import wx

class TodoAppVanilla(wx.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(None, *args, **kwargs)
        self.todo_items = []
        self.add_button = wx.Button(self, label='Add')
        self.textctrl = wx.TextCtrl(self)

        self.do_layout()

    def do_layout(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetSizer()



