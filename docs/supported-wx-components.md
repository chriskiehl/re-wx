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
 * [Dropdown](#ComboBox)
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
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |
|on_click | callable | Calls the supplied function when this element is click. | 

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
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |
|on_click | callable | Calls the supplied function when this element is click. |
 


<br/>

## Block

Block is a wrapped version of `wx.Panel` which automatically adds children to an internal [`wx.BoxSizer()`](https://www.wxpython.org/Phoenix/docs/html/wx.BoxSizer.html). This is the bread and butter of layout control in re-wx. Think of it as a `div` in HTML. 

**Example:** 

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

**Available Props:** 


| key | Type | Description | 
|------|------|---------|
|orient| int | Controls the direction of the sizer. `wx.HORIZONTAL` or `wx.VERTICAL` | 
|background_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|foreground_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|font| wx.Font | Sets the Font used by this component and all of its children|
|name| str | Adds the supplied name to the generated wx instance. This'll show in wx.Inspector and makes debugging much easier |
|min_size| (int, int) | A tuple of (min_width, min_height). Use -1 to let WX auto-size the component.|
|max_size| (int, int) | A tuple of (max_width, max_height). Use -1 to let WX auto-size the component.|
|tooltip| str | Displays a string when the user hovers over the component | 
|show| boolean | Toggle whether this item is visible or not. |
|enabled| boolean | Enables/Disables the component. |
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |
|on_click | callable | Calls the supplied function when this element is click. |


<br/>

## Button 


<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/button.PNG">
</p>


Your basic button. 

**Example:**

```
def button_example(props):
    return create_element(Button, {'label': 'Click me!', 'on_click': props['handler']})
```

**Availble Props:**


| key | Type | Description | 
|------|------|---------|
|label| string | The label displayed on the button |
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
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |
|on_click | callable | Calls the supplied function when this element is click. | 









<br/>

## BitmapButton 


<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/bitmap-button.PNG">
</p>



BitmapButton is a button which uses an image rather than a text label. Use the `uri` prop to specify the image you want displayed. 

**Example:**

```
def button_example(props):
    return create_element(BitmapButton, {
        'uri': 'path/to/your/image.png', 
        'on_click': props['handler']})
```

**Availble Props:**


| key | Type | Description | 
|------|------|---------|
|uri| string | filepath to the image you want displayed. re-wx will handle loading it and turning it into a bitmap |
|background_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|foreground_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|name| str | Adds the supplied name to the generated wx instance. This'll show in wx.Inspector and makes debugging much easier |
|min_size| (int, int) | A tuple of (min_width, min_height). Use -1 to let WX auto-size the component.|
|max_size| (int, int) | A tuple of (max_width, max_height). Use -1 to let WX auto-size the component.|
|tooltip| str | Displays a string when the user hovers over the component | 
|show| boolean | Toggle whether this item is visible or not. |
|enabled| boolean | Enables/Disables the component. |
|style| any | style is context dependent |
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |
|on_click | callable | Calls the supplied function when this element is click. | 



<br/>

## CalendarCtrl 

<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/calendarctrl.PNG">
</p>


CalendarCtrl is a premade date-picker. 

**Example:**

```
def calendar_example(props):
    return create_element(CalendarCtrl, {
        'selected_date': datetime.now(), 
        'on_change': props['handle_change']})
```

**Availble Props:**


| key | Type | Description | 
|------|------|---------|
|selected_date| datetime | sets the value of the date selected in the  widget |
|display_holidays | boolean | toggles whether or not to display holidays on the calendar|
|allow_month_change | boolean | controls whether or not the calendar can change to different months | 
|on_change| callable | Calls the supplied function when the user changes the selected date| 
|background_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|foreground_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|name| str | Adds the supplied name to the generated wx instance. This'll show in wx.Inspector and makes debugging much easier |
|min_size| (int, int) | A tuple of (min_width, min_height). Use -1 to let WX auto-size the component.|
|max_size| (int, int) | A tuple of (max_width, max_height). Use -1 to let WX auto-size the component.|
|tooltip| str | Displays a string when the user hovers over the component | 
|show| boolean | Toggle whether this item is visible or not. |
|enabled| boolean | Enables/Disables the component. |
|style| any | style is context dependent |
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |
|on_click | callable | Calls the supplied function when this element is click. | 



<br /> 

## CheckBox 

<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/checkbox.PNG">
</p>


The humble checkbox. You give it a clickie, it goes on or off. 

**Example:**

```
def example(props):
    return create_element(CheckBox, {
        'value': True, 
        'on_change': props['handle_change']})
```

**Availble Props:**




| key | Type | Description | 
|------|------|---------|
|label| str | The label displayed next to the CheckBox |
|value| boolean | Whether the checkbox is selected (`True`) or not (`False`) |
|on_change | callable | Calls the supplied function when the checkbox is clicked | 
|background_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|foreground_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|font| wx.Font | Sets the Font used by this component and all of its children|
|name| str | Adds the supplied name to the generated wx instance. This'll show in wx.Inspector and makes debugging much easier |
|min_size| (int, int) | A tuple of (min_width, min_height). Use -1 to let WX auto-size the component.|
|max_size| (int, int) | A tuple of (max_width, max_height). Use -1 to let WX auto-size the component.|
|tooltip| str | Displays a string when the user hovers over the component | 
|show| boolean | Toggle whether this item is visible or not. |
|enabled| boolean | Enables/Disables the component. |
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |


<br /> 

## ComboBox

<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/combobox.PNG">
</p>

Alias: Dropdown

**Example:**

```
def example(props):
    return create_element(ComboBox, {
        'selected': props['selected'],
        'choices': ['one', 'two', 'three', 'four'],
        'on_change': props['handle_change']})
```

**Availble Props:**

| key | Type | Description | 
|------|------|---------|
|value| str | The value to display in the textctrl part of the dropdown |
|choices| [str] | A list of strings to display in the dropdown |
|on_change | callable | Calls the supplied function when an item in the dropdown is selected | 
|on_input | callable | calls the supplied function when the user types into the textctrl portion of the dropdown | 
|style | int | See available styles in the [WXPython docs](https://www.wxpython.org/Phoenix/docs/html/wx.ComboBox.html) |
|background_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|foreground_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|font| wx.Font | Sets the Font used by this component and all of its children|
|name| str | Adds the supplied name to the generated wx instance. This'll show in wx.Inspector and makes debugging much easier |
|min_size| (int, int) | A tuple of (min_width, min_height). Use -1 to let WX auto-size the component.|
|max_size| (int, int) | A tuple of (max_width, max_height). Use -1 to let WX auto-size the component.|
|tooltip| str | Displays a string when the user hovers over the component | 
|show| boolean | Toggle whether this item is visible or not. |
|enabled| boolean | Enables/Disables the component. |
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |


<br /> 

## Frame

<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/frame.PNG">
</p>

This is the bedrock window to which all other components attach. There must be at least one of these in order for WX to bootstrap its GUI, and should must be at the root of your component tree. 

**Example:**

```
def example(props):
    return create_element(Frame, {'title': 'Hello world!'})
```

Note: The frame doesn't have to be created or managed by re-wx. Because re-wx outputs vanilla WX objects after `render`ing, you can attach them to an existing frame created elsewhere in the traditional WX manner. 

```
app = wx.App() 
frame = wx.Frame(None, title='Hello world!') 
my_panel = render(my_elements, frame)
frame.Show()
app.MainLoop()

```


**Availble Props:**

| key | Type | Description | 
|------|------|---------|
|title| str | The text which displays in the program bar | 
|show | boolean | Whether or not to show the Frame | 
|icon_uri | str | File path to the icon to display in the program bar | 
|style | int | See available styles in the [WXPython docs](https://www.wxpython.org/Phoenix/docs/html/wx.Frame.html) |
|background_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|foreground_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|font| wx.Font | Sets the Font used by this component and all of its children|
|name| str | Adds the supplied name to the generated wx instance. This'll show in wx.Inspector and makes debugging much easier |
|min_size| (int, int) | A tuple of (min_width, min_height). Use -1 to let WX auto-size the component.|
|max_size| (int, int) | A tuple of (max_width, max_height). Use -1 to let WX auto-size the component.|
|tooltip| str | Displays a string when the user hovers over the component | 






<br /> 

## Gauge

<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/gauge.PNG">
</p>


**Example:**

```
def example(props):
    return create_element(ComboBox, {
        'selected': props['selected'],
        'choices': ['one', 'two', 'three', 'four'],
        'on_change': props['handle_change']})
```

**Availble Props:**

| key | Type | Description | 
|------|------|---------|
|value| int | The the current value of the gauge  |
|range| int | Sets the maximum value of the gauge |
|pulse| boolean | when `True`, ignores `value` and `range` props and pulses on/off |
|style | int | See available styles in the [WXPython docs](https://www.wxpython.org/Phoenix/docs/html/wx.Gauge.html) |
|background_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|foreground_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|font| wx.Font | Sets the Font used by this component and all of its children|
|name| str | Adds the supplied name to the generated wx instance. This'll show in wx.Inspector and makes debugging much easier |
|min_size| (int, int) | A tuple of (min_width, min_height). Use -1 to let WX auto-size the component.|
|max_size| (int, int) | A tuple of (max_width, max_height). Use -1 to let WX auto-size the component.|
|tooltip| str | Displays a string when the user hovers over the component | 
|show| boolean | Toggle whether this item is visible or not. |
|enabled| boolean | Enables/Disables the component. |
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |













<br/>

## Grid

Like, [Block](#Block), Grid is a wrapped version of `wx.Panel` which automatically adds children to an internal [`wx.GridSizer()`](https://wxpython.org/Phoenix/docs/html/wx.GridSizer.html). 

**Example:** 

```python
from components import Block, TextCtrl, Button

def example(props):
    return wsx(
      [Grid, {'orient': wx.VERTICAL},    
        [TextCtrl, {'on_change': props['my_handler']}],
        [Button, {'on_click': props['handle_submit']}]]
    )
```

**Available Props:** 


| key | Type | Description | 
|------|------|---------|
|cols| int | The number of columns in the grid | 
|gap|(int, int) | the size of the gap between grid items (`(horizontal, vertical)`) |
|background_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|foreground_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|font| wx.Font | Sets the Font used by this component and all of its children|
|name| str | Adds the supplied name to the generated wx instance. This'll show in wx.Inspector and makes debugging much easier |
|min_size| (int, int) | A tuple of (min_width, min_height). Use -1 to let WX auto-size the component.|
|max_size| (int, int) | A tuple of (max_width, max_height). Use -1 to let WX auto-size the component.|
|tooltip| str | Displays a string when the user hovers over the component | 
|show| boolean | Toggle whether this item is visible or not. |
|enabled| boolean | Enables/Disables the component. |
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |
|on_click | callable | Calls the supplied function when this element is click. |










<br /> 

## ListCtrl

<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/listctrl.PNG">
</p>

The `ListCtrl` in WX, while extremely powerful, has a super awkward and fiddly API. To tame this, re-wx only exposes a subset of the `ListCtrl`'s functionality and wraps it all up in a more declarative, straight forward API geared towards showing tables of information. However, if you need the full, unadultered power of `ListCtrl`, you can always use a `Ref` to grab a handle to the concrete wx instance. 


**Example:**

```
some_data = [
    {'name': 'Timmy',
     'age': 12,
     'occupation': 'Child'},
    {'name': 'Buzz',
     'age': 48,
     'occupation': 'Astronaut'},
    {'name': 'Cloud',
     'age': 28,
     'occupation': 'Avalanche'},
    {'name': 'Spike',
     'age': 27,
     'occupation': 'Bounty Hunter'},
]

column_definitions = [
    {'title': 'NAME', 'column': lambda item: item['name']},
    {'title': 'AGE', 'column': lambda item: str(item['age'])},
    {'title': 'NAME', 'column': lambda item: item['occupation']}
]

def listctrl_example(props):
    return create_element(ListCtrl, {
        'column_defs': column_definitions,
        'data': some_data})
```

**Understanding the `column_defs` and `data` props**

`data` is a list of any arbirary type. It could be a list of lists, list of maps, or any `List[A]`.  

`column_defs` is how you define (a) what the columns of your table are, and (b) how the individual items in that column gets formatted. It's expressed as a list of maps, where each item in the list represents a column in your table. The `title` is used as the Column Header, and the `column` key should be a function (`A -> String`) which transforms an individual item from `data` into string form for display in the table. 

**Availble Props:**

| key | Type | Description | 
|------|------|---------|
|column_defs| [{title, column}] | A list of column definitions specifying your column header and row fomatting functions |
|data| List[A] | A list of data to be displayed in the table |
|background_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|foreground_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|font| wx.Font | Sets the Font used by this component and all of its children|
|name| str | Adds the supplied name to the generated wx instance. This'll show in wx.Inspector and makes debugging much easier |
|min_size| (int, int) | A tuple of (min_width, min_height). Use -1 to let WX auto-size the component.|
|max_size| (int, int) | A tuple of (max_width, max_height). Use -1 to let WX auto-size the component.|
|tooltip| str | Displays a string when the user hovers over the component | 
|show| boolean | Toggle whether this item is visible or not. |
|enabled| boolean | Enables/Disables the component. |
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |










<br /> 

## Panel


A plain WX.Panel. For a version with an attached Sizer, checkout [Block](#Block). 

Panel takes a backseat in re-wx to other types which have baked in Sizers and children management. In re-wx, panel is commonly used just as a spacer element when fine tuning layouts.  

**Example:**

```
def panel_as_spacer(props):
    return wsx(
      [Block, {'orient': wx.HORIZONTAL},
        # proportion 1 means grow to consume all of the available space 
        # because this is in a Horizontal Block, it'll have the effect 
        # of right aligning our button 
        [Panel, {'proportion': 1}] 
        [Button, {'label': 'A am right aligned thanks to the Panel'}]]
    )
```


| key | Type | Description | 
|------|------|---------|
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
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |
|on_click | callable | Calls the supplied function when this element is click. | 









<br /> 

## RadioBox

<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/radiobox.PNG">
</p>

Usage note: Because of how manages `RadioBox`, its items can _not_ be modified after creation. So, changing `choices` will unfortunately have no effect. If you need the choices to be dynamically modifiable, checkout [RadioButton](#RadioButton)

You _must_ define and handle `on_change` in order for the component to be controlled and honor your `selected` prop.

**Example:**

```
def example(props):
    return wsx(
      [RadioBox, {
        'selected': 2
        'choices': ['A', 'B', 'C'],
        'on_change': props['handle_change']
        }]
    )
```


| key | Type | Description | 
|------|------|---------|
| selected | int | the index of the selected option | 
| choices | [str] | A list of string to be displayed as options | 
|on_change | callable | This function is called when the user interacts with the radiobox|
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
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |






<br /> 

## RadioButton

<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/radio-button.PNG">
</p>

An individual RadioButton. This should be used over [RadioBox ](#RadioBox) when you need fine-grained control over interactions and layout. 

**Example:**

```python
def example(props):
    return wsx(
      [c.StaticBox, {'label': 'My Radio options'},
         [c.Block, {'flag': wx.TOP, 'border': 20},
             [c.RadioButton, {'label': 'A', 'selected': False}],
             [c.RadioButton, {'label': 'B', 'selected': True}],
             [c.RadioButton, {'label': 'C', 'selected': False}],
             [c.RadioButton, {'label': 'D', 'selected': False}]]]
    )
```


| key | Type | Description | 
|------|------|---------|
| selected | int | the index of the selected option | 
|on_change | callable | This function is called when the user interacts with the radiobox|
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
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |






<br /> 

## Slider


<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/slider.PNG">
</p>

**Example:**

```
def example(props):
    return wsx(
      [Slider, {'value': 22, 
                'min': 0,
                'max': 100}],
    )
```


| key | Type | Description | 
|------|------|---------|
|value| int | Current value/position of the slider | 
|min | int | Minimum value available in the slider | 
|max | int | Maximum value available in the slider | 
|on_change| callable | This function is called when the slider changes position | 
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
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |
|on_click | callable | Calls the supplied function when this element is click. | 






<br /> 

## SpinCtrl


<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/spinctrl.PNG">
</p>

**Example:**

```
def example(props):
    return wsx(
      [SpinCtrl, {'value': 22, 
                'min': 0,
                'max': 100}],
    )
```


| key | Type | Description | 
|------|------|---------|
|value| int | Current value of the spin control | 
|min | int | Minimum value of the spin control | 
|max | int | Maximum value of the spin control | 
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
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |
|on_click | callable | Calls the supplied function when this element is click. | 







<br /> 

## SpinCtrlDouble


<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/spinctrl-double.PNG">
</p>

**Example:**

```
def example(props):
    return wsx(
      [SpinCtrlDouble, {'value': 22, 
                'min': 0,
                'max': 100,
                'digits': 20,
                'increment': 0.02}],
    )
```


| key | Type | Description | 
|------|------|---------|
|value| float | Current value of the spin control | 
|min | float | Minimum value of the spin control | 
|max | float | Maximum value of the spin control | 
|digits | int | Sets the maximum precision of the spin control|
|increment | float | Sets the increment amount used by the spin control | 
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
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |
|on_click | callable | Calls the supplied function when this element is click. | 












<br/>

## StaticBitmap


<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/staticbitmap.PNG">
</p>


Display a fixed image. 

**Example:**

```
def button_example(props):
    return create_element(StaticBitmap, {'uri': 'path/to/your/image.png'})
```

**Availble Props:**


| key | Type | Description | 
|------|------|---------|
|uri| string | filepath to the image you want displayed. re-wx will handle loading it and turning it into a bitmap |
|background_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|foreground_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|name| str | Adds the supplied name to the generated wx instance. This'll show in wx.Inspector and makes debugging much easier |
|min_size| (int, int) | A tuple of (min_width, min_height). Use -1 to let WX auto-size the component.|
|max_size| (int, int) | A tuple of (max_width, max_height). Use -1 to let WX auto-size the component.|
|tooltip| str | Displays a string when the user hovers over the component | 
|show| boolean | Toggle whether this item is visible or not. |
|enabled| boolean | Enables/Disables the component. |
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |
|on_click | callable | Calls the supplied function when this element is click. | 














<br/>

## StaticBox


<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/staticbox.PNG">
</p>


Wraps its children in a bordered box with a name. 

**Example:**

```python
def example(props):
    return wsx(
      [c.StaticBox, {'label': 'My Radio options'},
         [c.Block, {'flag': wx.TOP, 'border': 20},
             [c.RadioButton, {'label': 'A', 'selected': False}],
             [c.RadioButton, {'label': 'B', 'selected': True}],
             [c.RadioButton, {'label': 'C', 'selected': False}],
             [c.RadioButton, {'label': 'D', 'selected': False}]]]
    )
```


**Availble Props:**


| key | Type | Description | 
|------|------|---------|
|label | str | Text to display at the top of the box | 
|background_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|foreground_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|name| str | Adds the supplied name to the generated wx instance. This'll show in wx.Inspector and makes debugging much easier |
|min_size| (int, int) | A tuple of (min_width, min_height). Use -1 to let WX auto-size the component.|
|max_size| (int, int) | A tuple of (max_width, max_height). Use -1 to let WX auto-size the component.|
|tooltip| str | Displays a string when the user hovers over the component | 
|show| boolean | Toggle whether this item is visible or not. |
|enabled| boolean | Enables/Disables the component. |
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |
|on_click | callable | Calls the supplied function when this element is click. | 















<br/>

## StaticLine

Displays a Horizontal or Vertical line. 

> Usage Note: make sure to set appropriate `proportion` and `flag` props to ensure that the line actually grows to fill the space you expect. If you're not seeing any lines when using this control, most of the time it's because your sizer isn't configured appropriately. Protip: Use the wx.Inspect tool! 

**Example:**

```python
def example(props):
    return wsx(
      [c.StaticLine, {'style': wx.SL_HORIZONTAL, 'proportion': 1}]
    )
```


**Availble Props:**


| key | Type | Description | 
|------|------|---------|
|style | str | Text to display at the top of the box | 
|background_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|foreground_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|name| str | Adds the supplied name to the generated wx instance. This'll show in wx.Inspector and makes debugging much easier |
|min_size| (int, int) | A tuple of (min_width, min_height). Use -1 to let WX auto-size the component.|
|max_size| (int, int) | A tuple of (max_width, max_height). Use -1 to let WX auto-size the component.|
|tooltip| str | Displays a string when the user hovers over the component | 
|show| boolean | Toggle whether this item is visible or not. |
|enabled| boolean | Enables/Disables the component. |
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |
|on_click | callable | Calls the supplied function when this element is click. | 














<br/>

## StaticText


<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/statictext.PNG">
</p>


A basic text element. This is the main way to display strings in a WX application. 

**Example:**

```python
def example(props):
    return wsx([StaticText, {'label': 'Hello world!'}])
```


**Availble Props:**


| key | Type | Description | 
|------|------|---------|
|Label | str | The text to be displayed|
|style | int | [See the WXPython docs for style options](https://www.wxpython.org/Phoenix/docs/html/wx.StaticText.html)| 
|background_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|foreground_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|name| str | Adds the supplied name to the generated wx instance. This'll show in wx.Inspector and makes debugging much easier |
|min_size| (int, int) | A tuple of (min_width, min_height). Use -1 to let WX auto-size the component.|
|max_size| (int, int) | A tuple of (max_width, max_height). Use -1 to let WX auto-size the component.|
|tooltip| str | Displays a string when the user hovers over the component | 
|show| boolean | Toggle whether this item is visible or not. |
|enabled| boolean | Enables/Disables the component. |
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |
|on_click | callable | Calls the supplied function when this element is click. | 








<br/>

## TextCtrl

<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/textctrl.PNG">
</p>


**Example:**

```python
def example(props):
    return wsx([TextCtrl, {'value': 'Hello world!'}])
```


**Availble Props:**


| key | Type | Description | 
|------|------|---------|
|value | str | The current text value of the control |
|placeholder| string | The hint text to display when the control is empty|
|editable| boolean | When false makes the control readonly|
|on_change| callable | This function will be called when the user enters text|
|style | int | [See the WXPython docs for style options](https://www.wxpython.org/Phoenix/docs/html/wx.TextCtrl.html)| 
|background_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|foreground_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|name| str | Adds the supplied name to the generated wx instance. This'll show in wx.Inspector and makes debugging much easier |
|min_size| (int, int) | A tuple of (min_width, min_height). Use -1 to let WX auto-size the component.|
|max_size| (int, int) | A tuple of (max_width, max_height). Use -1 to let WX auto-size the component.|
|tooltip| str | Displays a string when the user hovers over the component | 
|show| boolean | Toggle whether this item is visible or not. |
|enabled| boolean | Enables/Disables the component. |
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |
|on_click | callable | Calls the supplied function when this element is click. | 









<br/>

## TextArea

<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/textctrl.PNG">
</p>


This is an alias for TextCtrl, but with its `style` prop pre-baked with `wx.TE_MULTILINE`. 


**Example:**

```python
def example(props):
    return wsx([TextArea, {'value': 'Hello world!'}])
```


**Availble Props:**


| key | Type | Description | 
|------|------|---------|
|value | str | The current text value of the control |
|placeholder| string | The hint text to display when the control is empty|
|editable| boolean | When false makes the control readonly|
|on_change| callable | This function will be called when the user enters text|
|style | int | [See the WXPython docs for style options](https://www.wxpython.org/Phoenix/docs/html/wx.TextCtrl.html)| 
|background_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|foreground_color| rgb value | Either an rgb tuple (e.g. `(255, 255, 255)` or a hex string (e.g. `"#ff00ff"`)|
|name| str | Adds the supplied name to the generated wx instance. This'll show in wx.Inspector and makes debugging much easier |
|min_size| (int, int) | A tuple of (min_width, min_height). Use -1 to let WX auto-size the component.|
|max_size| (int, int) | A tuple of (max_width, max_height). Use -1 to let WX auto-size the component.|
|tooltip| str | Displays a string when the user hovers over the component | 
|show| boolean | Toggle whether this item is visible or not. |
|enabled| boolean | Enables/Disables the component. |
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |
|on_click | callable | Calls the supplied function when this element is click. | 










<br/>

## ToggleButton 


<p align="center">
    <img src="https://github.com/chriskiehl/re-wx-images/raw/images/wx_components/toggle-button.PNG">
</p>


Your basic button. 

**Example:**

```
def button_example(props):
    return create_element(Button, {'label': 'Click me!', 'on_click': props['handler']})
```

**Availble Props:**


| key | Type | Description | 
|------|------|---------|
|label| string | The label displayed on the button |
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
|proportion | int |  This parameter controls how much space this element will take up along the main axis of its parent sizer. 0 means don't grow at all, values > 0 cause it to scale proportionally relative to items with the same parent. See the [wx.Sizer docs for more info](https://www.wxpython.org/Phoenix/docs/html/sizers_overview.html#sizers-overview) |
|flag | int | An ORd combination of flags which control the Sizer's behavior  (e.g. `{'flag': wx.LEFT \| wx.RIGHT}`)|
|border | int | Sets the amount of border/padding which should be applied to the options specified in `flag` |
|on_click | callable | Calls the supplied function when this element is click. | 
