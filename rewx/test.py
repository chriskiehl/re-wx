"""
https://github.com/MrS0m30n3/youtube-dl-gui

"""
from wx.lib.pubsub import pub
import wx
from functools import partial
from pyrsistent import m, pmap, freeze, thaw
from copy import deepcopy
from random import randint, choice, random
from threading import Thread
from typing import Union
from uuid import uuid4

import os

import time

from rewx.rewx import Component, readit22
from subimpl import AppDB
from virtualdom import block22, textctrl, text22, textarea, button, dropdown, listctrl, bitmap, \
    bitmapbtn



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
    app = wx.App()
    wx.lib.inspection.InspectionTool().Show()
    frame = wx.Frame(None, title='Test re-wx')
    box = wx.BoxSizer(wx.VERTICAL)
    box.Add(root(frame))
    frame.SetSizer(box)
    frame.Show()
    frame.Fit()

    for child in frame.GetChildren():
        for ccc in child.GetChildren():
            for cc in ccc.GetChildren():
                cc.Layout()
            ccc.Layout()
        child.Layout()

    app.MainLoop()






class HomeScreen(Component):
    def __init__(self):
        super(HomeScreen, self).__init__()
        self.state = freeze({
            'text': 'Almost!',
            'name': str(uuid4()),
            'things': ['one', 'two', 'three', 'four']
        })


    def handle_click(self, event):
        self.setState(self.state.transform(['things'], lambda x: x.append(str(uuid4()))))

    def handle_itemclick(self, event):
        print('event is:', event)
        self.setState(self.state.transform(['things', eq(event)], str(uuid4())))


    def handle_change(self, event):
        print(event)
        self.setState(self.state.set('text', event.String))

    def render(self):
        # TODO: need a validation that children are proper elements if present
        return readit22(
            [block22, {'xid': 'blacktop'},
             [textctrl, {'xid': 'tctrl', 'value': 'Hello'}],
             [textctrl, {'xid': 'tctrl2', 'value': self.state.text, 'on_change': self.handle_change}],
             [text22, {'xid': 'foo', 'value': 'CLICK ME!', 'on_click': self.handle_click}],
             *[[text22, {'xid': thing, 'value': thing, 'on_click': callwith(self.handle_itemclick, thing)}]
               for thing in self.state['things']]]
        )


    def render2(self):
        return {
            'type': 'block',
            'attrs': {'xid': 'blockone'},
            'children': [{
                'type': 'statictext',
                'attrs': {
                    'value': 'CLICK TO ADD MORE!',
                    'on_click': self.handle_click,
                    'xid': 't1',
                },
                'children': []
            }] + [{
                'type': 'statictext',
                'attrs': {
                    'value': thing,
                    'on_click': callwith(self.handle_itemclick, thing),
                    'xid': thing,
                },
                'children': []
            } for thing in self.state['things']]
        }





def main():
    homescreen = YoutubeDownloader()
    app('Title', homescreen)




if __name__ == '__main__':
    main()