import wx
from unittest import TestCase

from rewx.components import NotebookItem
from rewx import mount, create_element
from rewx import components


def exclude(m, keys):
    return {k: v for k,v in base_props.items()
           if k not in keys}

base_props = {
    'label': 'some label',
    'value': 'some value',
    'background_color': '#ff00ff',
    'foreground_color': '#ff00ff',
    'font': wx.Font(),
    'helptext': 'some help text',
    'name': type.__name__,
    'min_size': (100, 100),
    'max_size': (200, 200),
    'tooltip': 'Tool tip here!',
    'enabled': True,
    'show': True,
}

valid_props = {
    wx.ListCtrl: {
        **exclude(base_props, {'value', 'background_color'}),
        'column_def': [],
        'data': []
    },
    wx.Panel: {
        **exclude(base_props, {'value'}),
    },
    wx.RadioBox: {
        **exclude(base_props, {'value'}),
        'on_change': lambda *args, **kwargs: None,
        'selected': 1,
        'choices': ['one', 'two'],
        'enabled_items': [0, 1]
    },
    wx.RadioButton: {
        **exclude(base_props, {'value'})
    },
    wx.ListBox: {
        **exclude(base_props, {'value'}),
        'choices': ['a', 'b'],
        'selected': [0, 1]
    },
    wx.Gauge: {
        **base_props,
        'value': 1
    },
    wx.Slider: {
        **base_props,
        'value': 10,
        'min': 0,
        'max': 1000
    },
    wx.SpinCtrl: {
        **base_props,
        'value': 10,
        'min': 0,
        'max': 1000
    },
    wx.SpinCtrlDouble: {
        **base_props,
        'value': 10,
        'min': 0,
        'max': 1000,
        'increment': 0.01,
        'digits': 5
    },
    wx.Notebook: {
        **exclude(base_props, {'value'})
    },
    wx.StaticBox: {
        **exclude(base_props, {'value'})
    },
    wx.StaticLine: {
        **exclude(base_props, {'value'})
    },
    wx.StaticText: {
        **exclude(base_props, {'value'})
    },
    components.Grid: {
        **exclude(base_props, {'value'})
    },
    components.Block: {
        **exclude(base_props, {'value'})
    }
}



class TestWidgets(TestCase):

    def get_defined_components(self):
        required_props = (
            NotebookItem,
        )
        return [
            obj for name, obj in components.__dict__.items()
            if name[0].isupper() and obj not in required_props]

    def empty_element(self, type):
        return create_element(type, {})

    def populated_element(self, type):
        return create_element(type, valid_props.get(type, {**base_props}))

    def test_empty_mounting(self):
        """
        Testing that all supported WX Primitives can
        be mounted without additional supporting props (excluding
        the RadioBox case).
        """
        app = wx.App()
        parent = wx.Frame(None)
        for element in map(self.empty_element, self.get_defined_components()):
            with self.subTest(element):
                # RadioBox doesn't allow constructions without `choices`
                # being present
                if element['type'] == wx.RadioBox:
                    element['props']['choices'] = ['a', 'b', 'c']
                instance = mount(element, parent)
                self.assertIsNotNone(instance)
                self.assertIsInstance(instance, element['type'])


    def test_basic_props(self):
        app = wx.App()
        parent = wx.Frame(None)
        for element in map(self.populated_element, self.get_defined_components()):
            with self.subTest(element):
                # RadioBox doesn't allow constructions without `choices`
                # being present
                if element['type'] == wx.RadioBox:
                    element = self.populated_element(wx.RadioBox)
                    element['props']['choices'] = ['a', 'b', 'c']
                elif element['type'] == wx.CheckBox:
                    element = self.populated_element(wx.CheckBox)
                    element['props']['value'] = True
                instance = mount(element, parent)
                self.assertIsNotNone(instance)
                self.assertIsInstance(instance, element['type'])