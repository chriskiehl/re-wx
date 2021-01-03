import wx

from widgets import mount


def render(element, parent):
    if issubclass(element['type'], wx.Object):
        return mount(element, parent)
    elif type(element['type']) == type:
        return element['type'].Render(element, parent)
    elif callable(element['type']):
        # stateless functional component
        return render(element['type'](element['props']), parent)
    else:
        raise Exception('UNKNOWN TYPE OF THING!!!')
        # instance: wx.Panel = block2wx(element, parent)
        # sizer = instance.GetSizer()
        # for child in element['props'].get('children'):
        #     sizer.Add(
        #         render(child, instance),
        #         child['props'].get('proportion', 0),
        #         child['props'].get('flag', 0),
        #         child['props'].get('border', 0)
        #     )
        # return instance