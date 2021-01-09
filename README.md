<p align="center">
  <img src="https://github.com/chriskiehl/re-wx-images/raw/images/logo/rewx.png"> 
</p>

<p align="center">A Python library for building modern declarative desktop applications</p>

<hr/>

![PyPI](https://img.shields.io/pypi/v/gooey)


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

## Installation 

The latest stable version is available on PyPi. 
```
pip install rewx 
```

## Documentation 

* [Tutorial: Intro to re-wx](#TODO)
* [Main Concepts ](#TODO)
* [Advanced Concepts](#TODO)
* [Components](#TODO)
* [Debugging](#TODO) 
* [Getting Help](#TODO) 


## re-wx in 5 minutes

re-wx has just a few core ideas: Elements, Components, and rendering. Everything else is achieved by combining these 3 ideas into larger and larger things. 
3 things 

A re-wx application consists of three steps. 

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
    frame.Show()
    app.MainLoop()
```

Run this and you'll see the output on the right. While not glamorous yet, it lets us explore several of the main ideas. 

At the heart of all re-wx applications is the humble `Element`. We used the function `create_element` to build them. Applications are built by composing trees of these elements together into larger and larger composite structures. 

Here we've created two elements. A top-level `Frame` type, which is required by WXPython, and then an inner `StaticText` one, which displays text on the screen. 

Elements all consist of three pieces of data: 1. the `type` of the entity we want to render into the UI, 3. the properties ("props" from here on out) we want that entity to have, and 3. any children, which are themselves Elements. 

An important note is that Elements are _plain data_ -- literally just a Python map. Together, they make up the "virtualdom" used by re-wx uses to drive the underlying WXWidgets components. Creating an element _does not_ instantiate any WX elements. That job falls to `render` 

`rewx.render` is how we transform our tree of Elements into a live UI. It handles all of the lifting required to instantiate the WX Objects, associate them all together, and put them in the state specified by your tree. The output of `render` is a WX Object, which in our case, is our top level frame. 

With the frame now happily created, we just have to tell WXPython to start its main loop, which will launch the GUI, and we've officially built our first re-wx app! 

### A brief detour for WSX:

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


<br/><br/>
### A Stateful component 

<img src="https://github.com/chriskiehl/re-wx-images/raw/images/screenshots/clock.png" align=right >

Components allow you to store and manage state. 

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
```




<br/><br/>
### An Application

<img src="https://github.com/chriskiehl/re-wx-images/raw/images/screenshots/todo-app.png" align=right >

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





## Examples: 

Here are a few samples of the applications availble in the [Examples Repo](#TODO). Check it out and contribute your own re-wx application demos! 

| Flat Layout | Column Layout |Success Screen | Error Screen | Warning Dialog |
|-------------|---------------|---------------|--------------|----------------|
| <img src="https://cloud.githubusercontent.com/assets/1408720/7950190/4414e54e-0965-11e5-964b-f717a7adaac6.jpg"> | <img src="https://cloud.githubusercontent.com/assets/1408720/7950189/4411b824-0965-11e5-905a-3a2b5df0efb3.jpg"> | <img src="https://cloud.githubusercontent.com/assets/1408720/7950192/44165442-0965-11e5-8edf-b8305353285f.jpg"> | <img src="https://cloud.githubusercontent.com/assets/1408720/7950188/4410dcce-0965-11e5-8243-c1d832c05887.jpg"> | <img src="https://cloud.githubusercontent.com/assets/1408720/7950191/4415432c-0965-11e5-9190-17f55460faf3.jpg"> | 

<h2 align="center">RE-WX in Action!</h2>









## Philosophy

**It's a library first.**
re-wx is "just" a library, _not_ a framework. Beacuse it's a library, you can use as much or as little of as you need. It requires no application-level total buy in like a framwork would. You don't have to do everything the "re-wx way. Further, the output from a re-wx `render` is a plain old WXPython component. Meaning, all re-wx components _ARE_ WX components, and thus require no special handling to integrate with your existing code base. 

**It's intended to be symbiotic with WXPython** 
re-wx is not trying to be an general purpose abstraction over multiple backend UI kits. It's lofty goals begin and end with it being a way of making writing native, cross-platform UIs in WXPython easier. As such, it doesn't need reconcilers, or generic transactions, or any other bloat. re-wx's entire codebase is just a handful of files < 1k lines of code, and could be understood in an afternoon.  

As such, practicality is favored over purity of abstraction. You'll mix and match WXPython code and re-wx code as needed. A good example of this is for transient dialogs (confirming actions, getting user selectsions, etc..). In React land, you'd traditionally have a modal in your core markup, and then conditionally toggle its visibility via state. However, in re-wx, you'll just use the dialog directly rather than embedding it in the markup and handling its lifecycle via `is_open` style state flags. This is practical to do because, unlike React in Javascript, WX handles managing the UI thread thus allowing us to block in place without any negative effects. Which enables writing straight forward in-line Dialog code.  

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

Open an issue [here]()
Or feel free to hit me up at me@chriskiehl.com


## Contributing

All contributions are welcome! Just make sure you follow the Contributing Guidelines. 


## License

re-wx is MIT licensed.
