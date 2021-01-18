
<p align="center">
  <img src="https://github.com/chriskiehl/re-wx-images/raw/images/logo/icon-large.png" align=center >
</p>

<h1 align="center">Debugging Guide</h1>
<br/><br/>


Writing massive applications leaves a lot of room for we failable humans to get a few things wrong. Luckily, WXPython comes with an awesome builtin debugging tool called [InspectionTool](https://www.wxpython.org/Phoenix/docs/html/wx.lib.mixins.inspection.html). This'll walk you though using it with re-wx. 

## Launching the Inspection Tool 

The tool is its own top-level Frame independent of yours, so you can create the InspectionTool anywhere as long as it's after the creation of `wx.App`. 

```
def main(): 
    app = wx.App()
    import wx.lib.inspection
    wx.lib.inspection.InspectionTool().Show()
    # rest of your code here
```

This'll launch the the Inspection Tool, which looks like this: 

<p align="center">
  <img src="https://github.com/chriskiehl/re-wx-images/raw/images/docs/debugging/inspector.png" align=center >
</p>

## Using `name` to identify Elements in the debugger

All builtin re-wx componets take a prop called `name`. When supplied, it will tag the wx components with that name in the debugger. This makes it much easier to find specific blocks is a large application. 

```python
def render():
    return wsx([StaticText, {'name': 'My Clock', ...}])
```


<p align="center">
  <img src="https://github.com/chriskiehl/re-wx-images/raw/images/docs/debugging/named-components.png" align=center >
</p>




