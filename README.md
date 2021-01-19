<p align="center">
  <img src="https://github.com/chriskiehl/re-wx-images/raw/images/logo/rewx.png"> 
</p>

<p align="center">A Python library for building modern declarative desktop applications</p>

<hr/>

<table>
  <tr>
    <td>
      <img src="https://github.com/chriskiehl/re-wx-images/raw/images/screenshots/basic-video-player.PNG"/>
    </td>
    <td>
      <img src="https://github.com/chriskiehl/re-wx-images/raw/images/screenshots/color-picker.png"/>
    </td>
    <td>
      <img src="https://github.com/chriskiehl/re-wx-images/raw/images/screenshots/kitchen-sink.png" />
    </td>
    <td>
      <img src="https://github.com/chriskiehl/re-wx-images/raw/images/screenshots/clock.png" />
    </td>
    <td>
      <img src="https://github.com/chriskiehl/re-wx-images/raw/images/screenshots/linux-youtube-dl.PNG" />
    </td>
  </tr>
</table

![PyPI](https://img.shields.io/pypi/v/re-wx)


# Overview

re-wx is a library for building modern declarative desktop applications. It's built as a management layer on top of WXPython, which means you get all the goodness of a mature, native, cross-platform UI kit, wrapped up in a modern, React inspired API. 

## What is it? 

It's a "virtualdom" for WX. You tell re-wx what you want to happen, and it'll do all the heavy lifting required to get WX to comply. It lets you focus on your state and business logic while leaving implentation details of WX's ancient API to re-wx.  

**Say goodbye to** 

* Deep coupling of business logic to stateful widgets
* Awkward auto-generated Python wrappers on old bloated C++ classes 
* Being forced to express UIs through low level `A.GetLayout().addChild(B)` style plumbing code 

**re-wx is:**

* Declarative
* Component Based 
* 100% compatible with all WXPython code bases

Re-wx lets you build expressive, maintainable applications out of simple, testable, functions and components.

## Alpha Note: 

This is an early release and under active development. Expect a few bugs, feature gaps, and a bit of API instability. If you hit any snags, pop over to the [issues](https://github.com/chriskiehl/re-wx/issues) and let me know!


## Installation 

The latest stable version is available on PyPi. 
```
pip install re-wx 
```

## Documentation 

* [Quick Start](#Quick-Start-RE-WX-in-5-minutes)
* [Main Concepts ](https://github.com/chriskiehl/re-wx/blob/main/docs/main-concepts.md)
* [Supported Components](https://github.com/chriskiehl/re-wx/blob/main/docs/supported-wx-components.md)
* [Debugging](https://github.com/chriskiehl/re-wx/blob/main/docs/debugging.md) 
* [Getting Help](#stuck-need-some-help-just-have-a-question) 


## Quick Start: RE-WX in 5 minutes

re-wx has just a few core ideas: Elements, Components, and rendering. Everything else is achieved by combining these 3 ideas into larger and larger things. 

All re-wx application consists of just a few steps. 

1. define your application view
2. Rendering  it to produce a wx object
3. kick off the wx Main Loop. 


### Starting small: Hello World

<img src="https://github.com/chriskiehl/re-wx-images/raw/images/screenshots/hello-world.png" align=right >

```python
import wx
from rewx import create_element, wsx, render     
from rewx.components import StaticText, Frame

if __name__ == '__main__':
    app = wx.App()    
    element = create_element(Frame, {'title': 'My Cool Application', 'show': True}, children=[
        create_element(StaticText, {'label': 'Howdy, cool person!'})
    ])
    frame = render(element, None)
    app.MainLoop()
```

Run this and you'll see the output on the right. While not glamorous yet, it lets us explore several of the main ideas. 

At the heart of all re-wx applications is the humble `Element`. We used the function `create_element` to build them. Applications are built by composing trees of these elements together into larger and larger composite structures. 

Here we've created two elements. A top-level `Frame` type, which is required by WXPython, and then an inner `StaticText` one, which displays text on the screen. 

Elements all consist of three pieces of data: 1. the `type` of the entity we want to render into the UI, 3. the properties ("props" from here on out) we want that entity to have, and 3. any children, which are themselves Elements. 

An important note is that Elements are _plain data_ -- literally just a Python dict like this: 

```python
{
  'type': Frame, 
  'props': {
      'title': 'My Cool Application', 
      'show': True,
      'children': [{
        'type': StaticText,
        'props': {'label': 'Howdy, cool person!'}
      }]
  }
```


Together, these elements make up the "virtualdom" used by re-wx uses to drive the underlying WXWidgets components. Creating an element _does not_ actually instantiate any WX elements. That job falls to `render` 

`rewx.render` is how we transform our tree of Elements into a live UI. It handles all of the lifting required to instantiate the WX Objects, associate them all together, and put them in the state specified by your tree. The output of `render` is a WX Object, which in our example, is our top level frame. 

With the frame now happily created, we just have to tell WXPython to start its main loop, which will launch the GUI, and we've officially built our first re-wx app! 

#### A brief detour for WSX:

Writing all those `create_element` statements can get really tedious and creates a lot of visual noise which can make getting a feel for your UI's structure at a glance difficult. An alternative and recommended approach is to use `wsx`, which lets you use nested lists to express parent child relationships between components. It uses the exact same `[type, props, *children]` arguments as `create_element`, but with a terser more compact syntax. Here's the same example using `wsx`. 

```python 
from rewx import wsx 
...
element = wsx(
  [Frame, {'title': 'My Cool Application', 'show': True}, 
    [StaticText, {'label': 'Howdy, cool person!'}]]
)
```

For the rest of this guide, we'll be using the `wsx` form, but you can use `create_element` if you prefer. 


<br/>

### A Stateful component 

<img src="https://github.com/chriskiehl/re-wx-images/raw/images/screenshots/clock.png" align=right >

Components are how you store and manage state in re-wx. 

```python
class Clock(Component):
    def __init__(self, props):
        super().__init__(props)
        self.timer = None
        self.state = {
            'time': datetime.datetime.now()
        }

    def component_did_mount(self):
        self.timer = wx.Timer()
        self.timer.Notify = self.update_clock
        self.timer.Start(milliseconds=1000)

    def update_clock(self):
        self.set_state({'time': datetime.datetime.now()})

    def render(self):
        return wsx(
          [c.Block, {},
           [c.StaticText, {'label': self.state['time'].strftime('%I:%M:%S'),
                           'name': 'ClockFace',
                           'foreground_color': '#51acebff',
                           'font': big_ol_font(),
                           'proporton': 1,
                           'flag': wx.CENTER | wx.ALL,
                           'border': 60}]]
        )
        
if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, title='Clock')
    clock = render(create_element(Clock, {}), frame)
    frame.Show()
    app.MainLoop()        
```

Here we've setup a Component which keeps track of the current time and displays it nice and bold in the center of our frame. 

There's lot going on here, so we'll take if from the top! 

You define your own components by inheriting from `rewx.Component`. This gives you access to all the lifecycle and state management options provided by the base class. You can checkout the [Main Concepts](https://github.com/chriskiehl/re-wx/blob/main/docs/main-concepts.md) for the full details of the life cycle methods.

Components have a few notable methods: 

| Method | Usage | 
|--------|-------|
| `__init__` | This gets called when re-wx instantiates your class. This is where you specify your initial state. Note that this is called _before_ the actual GUI elements are available. This method should be used only to initialize data, not deal with presentational concerns |
| `render` | This is where you'll create your element tree which defines your UI. | 
| `component_did_mount` | This method is called once all of your Component's elements have been rendered and mounted onto a wx.Window. It's here that you can kick off any work which requires the GUI to be up and running|
| set_state | This method is used update your components state and kick off a re-render of its visuals.| 

**Still just an element**

You use your component like any other Element we've encountered so far. Meaning, you don't instantiate it directly, you put in in your Element tree and let re-wx handle all the details. 

That's what we're doing down at the bottom of the file where we wire the app together. We create an Element from our Component just like normal: `create_element(Clock, {})` and pass it to our render function. 

```
if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, title='Clock')
    clock = render(create_element(Clock, {}), frame)
    frame.Show()
    app.MainLoop()  
```    
   
<br/>

### An Application

<img src="https://github.com/chriskiehl/re-wx-images/raw/images/screenshots/todo-app.png" align=right >

Our final example will pull it all together. It combines plain Elements, Components, and business logic into a complete application. 
```python 
def TodoList(props):
    return create_element(c.Block, {}, children=[
        create_element(c.StaticText, {'label': f" * {item}"})
        for item in props['items']
    ])


class TodoApp(Component):
    def __init__(self, props):
        super().__init__(props)
        self.state = {'items': ['Groceries', 'Laundry'], 'text': ''}

    def handle_change(self, event):
        self.set_state({**self.state, 'text': event.String})

    def handle_submit(self, event):
        self.set_state({
            'text': '',
            'items': [*self.state['items'], self.state['text']]
        })

    def render(self):
        return wsx(
            [c.Frame, {'title': 'My First TODO app'},
             [c.Block, {'name': 'main-content'},
              [c.StaticText, {'label': 'What needs to be done?'}],
              [c.TextCtrl, {'value': self.state['text']}],
              [c.Button, {'label': 'Add', 'on_click': self.handle_submit}],
              [c.StaticText, {'label': 'TO DO:'}],
              [TodoList, {'items': self.state['items'], 'on_click': self.handle_complete}]]]
        )

if __name__ == '__main__':
    app = wx.App()
    frame = render(create_element(TodoApp, {}), None)
    frame.Show()
    app.MainLoop()
```

### Where to go from here? 

Checkout the docs folder for more detailed guides and walk throughs




## Philosophy

**It's a library first.**
re-wx is "just" a library, _not_ a framework. Beacuse it's a library, you can use as much or as little of as you need. It requires no application-level total buy in like a framwork would. You don't have to do everything the "re-wx way. Further, the output from a re-wx `render` is a plain old WXPython component. Meaning, all re-wx components _ARE_ WX components, and thus require no special handling to integrate with your existing code base. 

**It's intended to be symbiotic with WXPython** 
re-wx is not trying to be an general purpose abstraction over multiple backend UI kits. It's lofty goals begin and end with it being a way of making writing native, cross-platform UIs in WXPython easier. As such, it doesn't need reconcilers, or generic transactions, or any other abstraction related bloat. As a result, re-wx's core codebase is just a handful of files and can be understood in an afternoon.  

Given the symbiotic nature, practicality is favored over purity of abstraction. You'll mix and match WXPython code and re-wx code as needed. A good example of this is for transient dialogs (confirming actions, getting user selectsions, etc..). In React land, you'd traditionally have a modal in your core markup, and then conditionally toggle its visibility via state. However, in re-wx, you'll just use the dialog directly rather than embedding it in the markup and handling its lifecycle via `is_open` style state flags. This is practical to do because, unlike React in Javascript, WX handles managing the UI thread thus allowing us to block in place without any negative effects. Which enables writing straight forward in-line Dialog code.  

```python
def handle_choose_dir(self, event): 
    dlg = wx.DirDialog(None)
    if dlg.Show() == wx.ID_OK:
        self.setState({'directory': dlg.GetPath()})
``` 

## Compromises and caveats in the design

While you'll program in a declarative style and enjoy the benefits that one-way data flows bring, a caveat is that not all components technically follow the unidirectional dataflow. The design of WX and the native APIs means that certain events are only fired _after_ internal states have been updated. So, for components like `wx.ComboBox` and `wx.TextCtrl`, handlers don't have a chance to operate until the widgets themseves have completed their work. 

The good news is that in practice, this is generally something you'll never notice or need to worry about. All updates are all done inside of a Freeze/Thaw transaction, thus hiding any visual quirks or flicker which may have come from re-wx forcing WX back into the state you specify rather than its own internally managed one.   

**API Surface area:** 

Only the most common attributes are currently managed by declarative props (basically, most of what falls under `wx.Control`). For example, specifics such as `InsertionPoint`s in `TextCtrl`s are considered out of scope for rewx. `Ref`s act as a handy escape-hatch for when you need access to the full WX API. Be sure to checkout the [Componet Docs](TODO) for the full list of supported props. 

**Stubborn Widgets:**

Some WXPython widget, like the prefab RadioGroup, cannot have its number of options changed after creation. So, updating the `choices` prop will have no effect. Luckily, these components are few and far between, and usually have easy work arounds or alternatives. See the [Componet Docs](TODO) for more info.  



## Stuck? Need some help? Just have a question? 

Open an issue [here](https://github.com/chriskiehl/re-wx/issues/new/choose), or feel free to hit me up directly at me@chriskiehl.com and we'll get it sorted out! 


## Contributing

All contributions are welcome! Just make sure you follow the Contributing Guidelines. 


## License

re-wx is MIT licensed.
