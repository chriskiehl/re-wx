"""
https://github.com/MrS0m30n3/youtube-dl-gui

"""

import wx
from functools import partial
from pyrsistent import m, pmap
from copy import deepcopy
from threading import Thread
from typing import Union
from uuid import uuid4

from subimpl import AppDB



def noop(event):
    event.Skip()

def logevent(event):
    print(event)
    event.Skip()

def foobar(props):
    return 'hello!'


def div(*args, **kwargs):
    pass

def text(*args, **kwargs):
    pass

import wx.lib.inspection


ssubs = {}


def app(title, root):
    global globs
    app = wx.App()
    wx.lib.inspection.InspectionTool().Show()
    frame = wx.Frame(None, title='Test re-wx')
    box = wx.BoxSizer(wx.VERTICAL)
    soot = root(frame)
    print(spreadit(soot))
    box.Add(soot, 1, wx.EXPAND)
    frame.SetSizer(box)
    frame.Show()

    for child in frame.GetChildren():
        for ccc in child.GetChildren():
            for cc in ccc.GetChildren():
                cc.Layout()
            ccc.Layout()
        child.Layout()

    app.MainLoop()


def hello_world():
    return r.div({
        'id': 'foobar',
        'style': {'font-weight': 200},
        'children': [
            r.div({
                'onInput': lambda event: print(event)
            })
        ]
    })



def hello_world2():
    return [div,
              {'id': 'foobar',
               'style': {'font-weight': 200}},
              'Hellooooooo world!']


def hello_world3():
    return block({
        'dir': wx.HORIZONTAL,
        'children': [
            block({})
        ]
    })
    return div(
        id='123',
        children=[
            div(dir=wx.HORIZONTAL),
            tt('hello'),
            tt('hello')
        ])


def text2(text):
    def inner(parent):
        statictext = wx.StaticText(parent, label=text)
        return statictext
    inner.__tt__ = 'text'
    return inner





def sub_name(db):
    return db['name']

state = None


class sub(object):
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass

    def register(self):
        pass




def text3(attrs, sub):
    def updater(statictext, value):
        statictext.SetLabel(value)
        statictext.GetParent().Layout()

    def inner(parent):
        statictext = wx.StaticText(parent, label=sub)
        statictext.SetToolTip('Hey, this is neat!')
        statictext.Bind(wx.EVT_LEFT_DOWN, attrs.get('on_click', logevent))
        return statictext
    inner.__tt__ = 'text'
    return inner


def block(attrs, *body, **kwargs):
    def inner(parent):
        panel = wx.Panel(parent)
        box = wx.BoxSizer((attrs or {}).get('dir', wx.VERTICAL))
        if attrs.get('dir') == wx.HORIZONTAL:
            x = wx.StaticText(panel)
            box.Add(x, 0, wx.EXPAND)
        for elm in body:
            e = elm(panel)
            box.Add(e, 0, wx.EXPAND)
        panel.SetSizer(box)
        return panel
    inner.__tt__ = 'div'
    return inner



def input2(attrs, *body):
    def inner(parent):
        tc = wx.TextCtrl(parent)
        tc.SetHint(attrs.get('placeholder', ''))
        if attrs.get('secretId'):
            tc.secretId = attrs.get('secretId')
        return tc
    inner.__tt__ = 'input'
    return inner




def button(attrs, *body):
    def inner(parent):
        button = wx.Button(parent, label='click me!')
        button.Bind(wx.EVT_BUTTON, attrs.get('on_click', logevent))
        if attrs.get('secretId'):
            button.secretId = attrs.get('secretId')
        return button
    return inner


def hello_world3():
    return block(
        {'id': '1234',
         'style': {'font-weight': 200},
         'on_click': "foo"},
        text('Helloooooo world!'),
        block('Hello!'))


def readit(schema):
    if not schema:
        return None
    fn, *args = schema
    if fn.__name__ in ('text3', 'input2', 'button'):
        return fn(*args)
    else:
        attr, *body = args
        return fn(attr, *map(readit, body))

def spreadit(root: wx.Frame):
    if not root:
        return {}
    if hasattr(root, 'secretId'):
        return {root.secretId: root}
    items = {}
    for child in root.GetChildren():
        items.update(spreadit(child))
    return items



def readit22(schema):
    if not schema:
        return None
    fn, *args = schema
    if fn.__name__ in ('text22', 'input22', 'button22'):
        return fn(*args)
    else:
        attr, *body = args
        return fn(attr, *map(readit22, body))




def atom(state):
    return state


def form(attr, *body):
    return \
        [block, {'dir': wx.HORIZONTAL},
          [input2, {'placeholder': 'whoa!'}, 'hey'],
          [button, {}, 'hey']]


def application():
    return \
        [block, {},
          [text3, {}, "What's your name?"],
          [input2, {'secretId': 'myInput', 'placeholder': 'Enter your name here'}, ''],
          [block, {'dir': wx.HORIZONTAL},
           [button, {'secretId': 'okButton'}, 'hey'],
           [button, {'secretId': 'cancelButton'}, 'hey']]]


def handleUpdate(widgets):
    def handle(event):
        pass


class Foobar(wx.Panel):
    """
    Core problem with a "slightly better sizer" is that you need to
    have a handle to the components you want to interact with.

    If we go declarative where the framework instantiates the widgets, we have
    to fish them back out later, into either a map, which is awkard from a typing
    perspective, or we have to specify what components SHOULD be extracted, so that
    the IDE can help us code.

    OR we have to declare things ahead of time and then use them in the 'slightly better
    sizer' thus gaining almost no real advantage beyond removing a few lines of code.
    """
    def __init__(self, *args, **kwargs):
        super(Foobar, self).__init__(*args, **kwargs)
        self.input: wx.TextCtrl = None
        self.okButton: wx.Button = None
        self.cancelButton: wx.Button = None

    def render(self):
        return \
            [block, {},
              [text3, {}, 'What name are?'],
              [self.input],
              [block, {},
                [self.okButton]
                [self.cancelButton]]]

def foo(parent):
    root = readit(application())(parent)
    inputs = spreadit(root)

    button: wx.Button = inputs['myInput']



    print(spreadit(root))



def main():
    root = readit(application())
    app('Title', root)



if __name__ == '__main__':
    main()