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




**Example:**

```
def example(props):
    return create_element(ComboBox, {
        'selected': props['selected'],
        'choices': ['one', 'two', 'three', 'four'],
        'on_change': props['handle_change']})
```


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











