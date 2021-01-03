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

from rewx.rewx2 import Component, wsx, create_element, render
from rewx import components as c
from util import extend, veq



def fake_download(item):
    duration = randint(5,10)
    size_in_mb = randint(10, 100)
    speed = size_in_mb / float(duration)
    ext = choice(['.webm', '.mp4', '.m4a', '.h264'])
    last = time.time()
    end = last + duration
    downloaded = 0.0001
    if item is None:
        a = 10
    while time.time() < end:
        elapsed = time.time() - last
        downloaded += speed * elapsed
        xxx = item.update({
            'ext': ext,
            'speed': speed + randint(0, 100),
            'size': size_in_mb,
            'percent': float(downloaded) / size_in_mb,
            'status': 'Downloading',
            'eta': end - time.time(),
        })
        if xxx is None:
            a = 10

        wx.CallAfter(pub.sendMessage, 'download_update', item=item.update({
            'ext': ext,
            'speed': speed + randint(0, 100),
            'size': size_in_mb,
            'percent': float(downloaded) / size_in_mb,
            'status': 'Downloading',
            'eta': end - time.time(),
        }))
        last = time.time()
        time.sleep(random())
    wx.CallAfter(pub.sendMessage, 'download_update', item=item.update({
        'ext': ext,
        'speed': None,
        'size': size_in_mb,
        'status': 'Complete',
        'percent': 1,
        'eta': None,
    }))


class YoutubeDownloader(Component):
    def __init__(self, props):
        super().__init__(props)
        self.state = freeze({
            'urls': 'asdf\nqwer',
            'formats': ['mp4', 'mp3', 'm4a', 'vorbis'],
            'selected_format': 'mp3',
            'output_dir': r'C:\Users\Chris\Desktop\akira-bk',
            'status': 'READY',
            'downloads': [
                self.dload('youtube,com'),
                self.dload('google,com'),
                self.dload('bing,com'),

            ]
        })
        pub.subscribe(self.update_downloads, 'download_update')
        pub.subscribe(self.finish_downloads, 'downloads_complete')

    def update_downloads(self, item):
        print('update_downloads', self.state.status)
        self.set_state(self.state.transform(['downloads', veq('id', item['id'])], item))

    def finish_downloads(self, **kwargs):
        self.set_state(self.state.set('status', 'READY'))

    def handle_choose_fmt(self, event: wx.CommandEvent):
        # relevant event props: Selection, String
        print('handle_choose_fmt called', event)
        self.set_state(self.state.set('selected_format', event.String))

    def handle_add(self, event: wx.CommandEvent):
        if not self.state.urls:
            return wx.MessageBox("You haven't entered any URLs!", caption='Whoops!')
        if not os.path.exists(self.state.output_dir):
            return wx.MessageBox("Choose a valid output dir!", caption='Hey!')
        downloads = list(map(self.dload, self.state.urls.split('\n')))
        self.set_state(
            self.state
                .transform(['downloads'], extend(downloads))
                .set('urls', ''))

    def dload(self, url):
        return freeze({
            'id': str(uuid4()),
            'url': url,
            'ext': None,
            'size': None,
            'percent': 0,
            'eta': None,
            'speed': None,
            'status': 'Queued'
        })

    def handle_url_change(self, event):
        print(event.String)
        self.set_state(self.state.set('urls', event.String))

    def handle_choose_dir(self, event):
        dlg = wx.DirDialog(None, message='Hello?')
        if dlg.ShowModal() == wx.ID_OK:
            self.set_state(self.state.set('output_dir', dlg.GetPath()))

    def handle_start(self, event: wx.CommandEvent):
        self.set_state(self.state.set('status', 'DOWNLOADING'))
        t = Thread(target=self.run_downloads)
        t.start()

    def run_downloads(self):
        from multiprocessing.dummy import Pool
        pool = Pool(30)
        results = pool.map(fake_download, self.state.downloads)
        wx.CallAfter(pub.sendMessage, 'downloads_complete')


    def column_defs(self):
        def fmt_size(item):
            return f"{item['size']}MB" if item['size'] else '-'

        def fmt_time_remaining(item):
            return f"{round(item['eta'], 1)}s" if item['eta'] else '-'

        def fmt_speed(item):
            return f"{round(item['speed'], 2)}MB/s" if item['speed'] else '-'

        def fmt_percent(item):
            return f"{round(item['percent'] * 100, 2) }%" if item['percent'] else '-'

        return [
            {'title': 'URL', 'column': lambda x: x['url']},
            {'title': 'Extension', 'column': lambda x: x['ext'] or '-'},
            {'title': 'Size', 'column': fmt_size},
            {'title': 'Percent', 'column': fmt_percent},
            {'title': 'ETA', 'column': fmt_time_remaining},
            {'title': 'Speed', 'column': fmt_speed},
            {'title': 'Status', 'column': lambda x: x['status']}
        ]

    def is_downloading(self):
        print('is_downloading', self.state.status == 'DOWNLOADING')
        return self.state.status == 'DOWNLOADING'

    def run_icon(self):
        return './images/cloud_download_32px.png' \
            if self.state.status == 'READY' \
            else './images/folder_32px.png'


    def foo(self, event):
        self.set_state(self.state)

    def render(self):
        return wsx(
            [c.Dropdown, {'xid': 'fmt',
                          'on_change': self.handle_choose_fmt,
                          'on_input': self.foo,
                          'choices': self.state.formats,
                          'value': self.state.selected_format}]
        )
        return wsx(
            [c.Block, {},
             [c.Block, {'flag': wx.EXPAND | wx.ALL, 'border': 20},
              [c.StaticText, {'label': 'Enter URLs below'}],
              [c.TextArea, {'disabled': self.is_downloading(),
                            'value': self.state['urls'],
                            'flag': wx.EXPAND,
                            'on_change': self.handle_url_change}],
              [c.Block,
               {'orient': wx.HORIZONTAL, 'proportion': 0, 'flag': wx.EXPAND | wx.TOP | wx.BOTTOM,
                'border': 20},
               [c.StaticBitmap, {'uri': 'images/folder_32px.png'}],
               [c.TextCtrl, {'placeholder': 'choose output directory',
                             'disabled': self.is_downloading(),
                             'value': self.state.output_dir}],
               [c.Button, {'disabled': self.is_downloading(),
                           'label': 'browse',
                           'on_click': self.handle_choose_dir}],
               [c.Panel, {'proportion': 1}],
               [c.Dropdown, {'xid': 'fmt',
                             'on_change': self.handle_choose_fmt,
                             'choices': self.state.formats,
                             'value': self.state.selected_format}],
               [c.Button, {'xid': 'add', 'label': 'Add', 'on_click': self.handle_add}]],
              [c.Block, {'xid': 'dlist'},
               [c.StaticText, {'xid': '123', 'label': 'Download list'}],
               [c.ListCtrl,
                {'style': wx.LC_REPORT, 'column_defs': self.column_defs(),
                 'data': self.state.downloads}]],
              [c.Block, {'orient': wx.HORIZONTAL, 'flag': wx.EXPAND},
               [c.Panel, {'proportion': 1}],
               [c.BitmapButton, {'xid': 'start',
                                 'uri': self.run_icon(),
                                 'on_click': self.handle_start}]]]]
        )


def app(title, root):
    import wx
    app = wx.App()
    frame = wx.Frame(None, title='Test re-wx')
    import wx.lib.inspection
    wx.lib.inspection.InspectionTool().Show()
    thing = render(create_element(YoutubeDownloader, {}), frame)
    box = wx.BoxSizer(wx.VERTICAL)
    box.Add(thing, 1, wx.EXPAND)
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


def main():
    app('Youtube-DL', None)

if __name__ == '__main__':
    main()