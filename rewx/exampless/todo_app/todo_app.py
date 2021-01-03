from rewx.rewx2 import Component, wsx


def TodoList(props):
    """Stateless functional component"""
    return wsx(
        ['block', {},
         *[['statictext', {'label': f" * {item['text']}"}]
           for item in props['items']]]
    )

class TodoApp(Component):
    def __init__(self, props):
        super().__init__(props)
        self.state = {'items': [], 'text': ''}

    def handle_change(self, event):
        self.set_state({**self.state, 'text': event.String})

    def handle_submit(self, event):
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



if __name__ == '__main__':
    pass


