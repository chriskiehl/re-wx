import wx
from rewx import Component, wsx, render, create_element
from rewx.components import Block, Button, Gauge


class FooGauge(Component):
    def __init__(self, props):
        super().__init__(props)
        self.props = props
        self.state = {"counter": 1000}

    def update_count(self, event):
        self.set_state({"counter": self.state.get("counter", 0) + 100})

    def render(self):
        return wsx(
            [Block, {},
             [Gauge, {"value": self.state["counter"],
                      "range": 3000,
                      "name": "Counter",
                      "flag": wx.CENTER | wx.ALL,
                      "size": (5000, 200),  # How to set size of this Gauge?
                      "border": 30,
                      "pulse": False}],
             [Button, {"label": "Update",
                       "on_click": self.update_count,
                       "flag": wx.CENTER | wx.ALL}],
            ]
        )


if __name__ == "__main__":
    app = wx.App()

    import wx.lib.inspection
    wx.lib.inspection.InspectionTool().Show()

    frame = wx.Frame(None, title="Gauge With Update")
    clock = render(create_element(FooGauge, {}), frame)

    frame.Show()
    app.MainLoop()