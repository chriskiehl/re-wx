import wx
import rewx.virtualdom as v
from examples.gooey.gooey import Screens
from rewx.rewx import readit22
from itertools import zip_longest


def title_font():
    return wx.Font(10, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

def subtitle_font():
    return wx.Font(9, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)


def bold_font():
    return wx.Font(9, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)


def chunk(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def footer(props, *body):
    return readit22(
        [v.vblock22, {'xid': 'b1', 'proportion': 0, 'flag': wx.EXPAND, 'min_size': (-1, 53)},
         [v.block22, {'xid': 'b1', 'dir': wx.HORIZONTAL,
                      'flag': wx.EXPAND | wx.ALL, 'border': 10, 'background_color': '#f0f0f0'},
          *body]]
    )

def config_footer(props):
    return readit22(
        [footer, {},
         [v.text22, {'xid': 'spacer', 'value': '', 'proportion': 1, 'flag': wx.EXPAND}],
         [v.button, {'xid': 'srt', 'label': 'Cancel', 'on_click': props['on_cancel']}],
         [v.button, {'xid': 'cnl', 'label': 'Start', 'on_click': props['on_start'],
                     'flag': wx.LEFT, 'border': 10}]]
    )

def runtime_footer(props):
    return readit22(
        [footer, {},
         [v.gauge, {'xid': 'gauge', 'pulse': True,  'proportion': 0}]]
    )

def results_footer(props):
    return readit22(
        [footer, {},
         [v.text22, {'xid': 'spacer', 'value': '', 'proportion': 1, 'flag': wx.EXPAND}],
         [v.button, {'xid': 'edit', 'label': 'Edit', 'on_click': props['on_edit']}],
         [v.button, {'xid': 'rsart', 'label': 'Restart', 'on_click': props['on_restart']}],
         [v.button, {'xid': 'close', 'label': 'Close', 'on_click': props['on_close']}]]
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


def chooser(props, *body):
    return [v.block22, {'xid': 'chsr', 'dir': wx.HORIZONTAL, 'flag': wx.EXPAND},
            [v.textctrl, {'xid': props['xid'], 'value': props['value'], 'proportion': 1, 'on_change': props['on_change']}],
            [v.button, {'xid': 'chbtn', 'label': props['label'], 'flag': wx.LEFT, 'border': 5}]]



def www(props, children):
    return v.block22(
        children=[
            v.text22(value='hey'),
            v.text22(value='yp'),
            *children
        ]
    )


def two_columns(props, *body):
    """
    display all children in groups of two widgets
    """
    children = list(map(readit22, body))
    updated_children = []
    for c1, c2 in chunk(children, 2):
        c1['attrs'].update({'proportion': 1})
        if c2:
            c2['attrs'].update({'proportion': 1, 'flag': wx.LEFT, 'border': 20})
            updated_children.append(v.block22({'xid': 'g', 'dir': wx.HORIZONTAL, 'flag': wx.EXPAND | wx.TOP, 'border': 20}, c1, c2))
        else:
            updated_children.append(v.block22({'xid': 'g', 'dir': wx.HORIZONTAL, 'flag': wx.EXPAND | wx.TOP, 'border': 20}, c1))

    return v.block22({'xid': 'two-col', 'flag': wx.EXPAND | wx.TOP, 'border': 20}, *updated_children)


def widget(props, *body):
    return readit22(
      [v.block22, {'xid': 'widget', 'flag': wx.TOP | wx.EXPAND, 'border': 20},
       [v.text22, {'xid': 'a', 'value': props['label'], 'font': bold_font()}],
       [v.text22, {'xid': 'a', 'value': props['help']}],
       *body]
    )



def when(props, *body):
    if props['is_true']:
        return v.block22({'xid': props['xid'],'proportion': 1, 'flag': wx.EXPAND}, *map(readit22, body))
    else:
        return v.block22({'xid': 'n', 'proportion': 0})


def main_body(props, *body):
    if props['screen'] == Screens.CONFIG:
        return config_page(props)
    else:
        return readit22([v.textctrl, {'xid': '111', 'value': 'uhh'}])

def config_page(props):
    return readit22(
      [v.scrollblock, {'xid': 'confg', 'proportion': 1, 'flag': wx.EXPAND},
       [v.block22, {'xid': '12', 'proportion': 1, 'flag': wx.EXPAND | wx.ALL, 'border': 20},
        # Required args section
        [v.block22, {'xid': 'reqs', 'flag': wx.EXPAND | wx.BOTTOM, 'border': 30},
         [v.text22, {'xid': 'a', 'value': 'Required Arguments', 'font': title_font()}],
         [v.line, {'xid': 'rl', 'flag': wx.EXPAND}],
         [v.grid, {'xid': 'grid', 'cols': 1, 'gap': (20, 10), 'flag': wx.EXPAND},
          *[[widget, {'label': opt['label'], 'help': opt['help']},
             [chooser, {'xid': opt['id'],
                        'label': 'Browse',
                        'value': opt['value'],
                        'on_change': props['on_change']}]]
            for opt in props['required']]]],

        # Optional Args Section
        [v.block22, {'xid': 'reqs', 'flag': wx.EXPAND | wx.BOTTOM, 'border': 40},
         [v.text22, {'xid': 'a', 'value': 'Optional Arguments', 'font': title_font()}],
         [v.line, {'xid': 'rl', 'flag': wx.EXPAND}],
         [v.grid, {'xid': 'grid', 'cols': 2, 'gap': (20, 10), 'flag': wx.EXPAND},
          *[[widget, {'label': opt['label'], 'help': opt['help']},
             [v.textctrl, {'xid': opt['id'],
                           'value': opt['value'],
                           'flag': wx.EXPAND,
                           'on_change': props['on_change']}]]
            for opt in props['optional']]]]]]
    )
