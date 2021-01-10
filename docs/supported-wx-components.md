# Supported WX Components 



### Available Components: 

 * [ActivityIndicator](#ActivityIndicator)
 * [Block](#Block)
 * [Button](#Button)
 * [BitmapButton](#BitmapButton)
 * [CalendarCtrl](#CalendarCtrl)
 * [CheckBox](#CheckBox)
 * [CollapsiblePane](#CollapsiblePane)
 * [ComboBox](#ComboBox)
 * [Dropdown](#Dropdown)
 * [Frame](#Frame)
 * [Gauge](#Gauge)
 * [Grid](#Grid)
 * [ListBox](#ListBox)
 * [ListCtrl](#ListCtrl)
 * [Panel](#Panel)
 * [RadioBox](#RadioBox)
 * [RadioButton](#RadioButton)
 * [Slider](#Slider)
 * [SpinCtrl](#SpinCtrl)
 * [SpinCtrlDouble](#SpinCtrlDouble)
 * [StaticBitmap](#StaticBitmap)
 * [StaticBox](#StaticBox)
 * [StaticLine](#StaticLine)
 * [StaticText](#StaticText)
 * [SVG](SVG)
 * [SVGButton](SVGButton)
 * [TextArea](#TextArea)
 * [TextCtrl](#TextCtrl)
 * [ToggleButton](#ToggleButton)
 * [MediaCtrl](#MediaCtrl)



## How to use

WX Widgets supported and managed by re-wx can all be found in the `components` module. 

```python
from rewx import components as c 
```



TEMPLATE


| key | Type | Description | 
|------|------|---------|
|label| blah |
|value| blah |
|background_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|foreground_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|font| wx.Font | Sets the Font used by this component and all of its children|
|name| str | Adds the supplied name to the generated wx instance. This'll show in wx.Inspector and makes debugging much easier |
|min_size| (int, int) | A tuple of (min_width, min_height). Use -1 to let WX auto-size the component.|
|max_size| (int, int) | A tuple of (max_width, max_height). Use -1 to let WX auto-size the component.|
|tooltip| str | Displays a string when the user hovers over the component | 
|show| boolean | Toggle whether this item is visible or not. |
|enabled| boolean | Enables/Disables the component. |
|style| any | style is context dependent |


END TEMPLATE



## ActivityIndicator 

<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/activity-indicator.PNG">
</p>

**Official WXPython docs:**

**Example:** 

```
from components import ActivityIndicator

def example(props): 
    return create_element(ActivityIndicator, {'start': props['is_loading']})
```

**Available Props:** 

| key | Type | Description | 
|------|------|---------|
| start | boolean | Controls whether or not the spinner is animating |
|background_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|foreground_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|name| str | Adds the supplied name to the generated wx instance. This'll show in wx.Inspector and makes debugging much easier |
|tooltip| str | Displays a string when the user hovers over the component | 
|show| boolean | Toggle whether this item is visible or not. |
|enabled| boolean | Enables/Disables the component. |
|style| any | style is context dependent |
 



## Block

Block is a wrapped version of `wx.Panel` which automatically adds children to an internal [`wx.BoxSizer()`](https://www.wxpython.org/Phoenix/docs/html/wx.BoxSizer.html). This is the bread and butter of layout control in re-wx. Think of it as a `div` in HTML. 

Example: 

```python
from components import Block, TextCtrl, Button

def example(props):
    return wsx(
      [Block, {'orient': wx.VERTICAL},    
        [Block, {'orient': wx.HORIZONTAL, 'flag': wx.EXPAND}, 
          [TextCtrl, {'on_change': props['my_handler']}],
          [Button, {'on_click': props['handle_submit']}]]]
    )
```


