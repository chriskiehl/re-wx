import wx
import rewx.virtualdom as v
from rewx.rewx import readit22


# class Point2D(TypedDic):
#     x: int
#     y: int
#     label: str


def title_font():
    return wx.Font(10, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

def subtitle_font():
    return wx.Font(9, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)


def config_footer(props):
    return readit22(
        [v.vblock22, {'xid': 'b1', 'proportion': 0, 'flag': wx.EXPAND, 'min_size': (-1, 53)},
         [v.block22, {'xid': 'b1', 'dir': wx.HORIZONTAL, 'flag': wx.EXPAND | wx.ALL, 'border': 10,
                     'background_color': '#f0f0f0'},
           [v.text22, {'xid': 'spacer', 'value': '',  'proportion': 1, 'flag': wx.EXPAND}],
           [v.button, {'xid': 'srt', 'label': 'Cancel', 'on_click': props['on_cancel']}],
           [v.button, {'xid': 'cnl', 'label': 'Start',
                       'on_click': props['on_start'], 'flag': wx.LEFT, 'border': 10}]]]
    )

def runtime_footer(props):
    return readit22(
        [v.block22, {'xid': 'rft', 'dir': wx.HORIZONTAL},
         [v.gauge, {'xid': 'gauge', 'pulse': True}],
         [v.button, {'xid': 'stopbtn', 'label': 'Stop'}]]
    )

def finished_footer(props):
    return readit22(
        [v.block22, {'xid': 'rft', 'dir': wx.HORIZONTAL},
         [v.button, {'xid': 'edit', 'label': 'Edit'}],
         [v.button, {'xid': 'rsart', 'label': 'Restart'}],
         [v.button, {'xid': 'close', 'label': 'Close'}]]
    )


def header(props):
    return readit22(
     [v.block22, {'xid': 'header', 'dir': wx.HORIZONTAL,
                  'flag': wx.EXPAND, 'proportion': 1,
                   'background_color': '#ffffff',
                  'min_size': (-1, 80),
                  'max_size': (-1, 80)},
      [v.vblock22, {'xid': 'msgs', 'proportion': 1,'flag': wx.EXPAND | wx.ALL, 'border': 10},
       [v.text22, {'xid': 'title',
                   'value': props['title'],
                   'font': title_font()}],
       [v.text22, {'xid': 'subtitle', 'value': props['subtitle']}]],
      [v.bitmap, {'xid': 'bmp', 'uri': props['icon_uri'], 'flag': wx.CENTER | wx.RIGHT, 'border': 10}]]
    )

def textinput(props):
    return [v.textctrl, {'xid': props['value'], 'value': props['value']}]

def textinput(props):
    return [v.block22, {'xid': 'chsr', 'dir': wx.HORIZONTAL},
            [v.textctrl, {'xid': props['value'], 'value': props['value']}],
            [v.button, {'xid': props['value'], 'value': props['value']}]]


def config_page(props):
    return readit22(
      [v.scrollblock, {'xid': 'confg', 'proportion': 1, 'flag': wx.EXPAND},
       *[[v.text22, {'xid': str(e), 'value': 'Hello!'}]
         for e in range(13)]]
    )
