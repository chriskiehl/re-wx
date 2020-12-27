import wx
import wx.lib.inspection





class TodoLine(wx.Panel):
    def __init__(self, parent, label, *args, **kwargs):
        super(TodoLine, self).__init__(parent)
        self.textInput = wx.TextCtrl(self, value=label)
        self.completButton = wx.Button(self, label='Done!')
        self.deleteButton = wx.Button(self, label='Delete')

        # self.completButton.Bind(wx.EVT_BUTTON, self)
        # self.deleteButton.Bind(wx.EVT_BUTTON, self)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.textInput, 1)
        sizer.Add(self.completButton)
        sizer.Add(self.deleteButton)
        self.SetSizer(sizer)


class TodoModel(object):
    def __init__(self):
        self.todos = []

    def addTodo(self, todo):
        self.todos.append({'text': todo, 'completed': False})

    def removeTodo(self, todo):
        self.todos.remove(todo)

    def completeTodo(self, toUpdate):
        index = self.todos.index(toUpdate)
        self.todos[index] = {**self.todos[index], 'completed': True}

class TodoApp(wx.Frame):
    def __init__(self):
        super(TodoApp, self).__init__(None, title='Hello world!')

        self.items = []
        self.itemSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.itemSizer)
        self.SetSizer(self.sizer)

        self.addItem('one')
        self.addItem('Two')
        self.addItem('Three')

        self.Layout()

    def addItem(self, todo):
        line = TodoLine(self, todo)
        self.items.append(line)
        self.itemSizer.Add(line)
        # self.Layout()


def main():
    app = wx.App()
    frame = TodoApp()
    frame.Show()
    wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()



if __name__ == '__main__':
    main()