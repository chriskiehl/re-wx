# Main Concepts

* [Elements and Rendering](#Elements-and-rendering)
* [WSX](#WSX)
* [Rendering](#Rendering)
* [Creating reusable Elements](#Creating-reusable-Elements
* [Components](#Components)
* [Component and State](#Component-and-state)
* [Component lifecycle methods](#Component-lifecycle-methods)
* [Running re-wx Applications](#Running-re-wx-Applications)



### Knowledge Level Assumptions 

re-wx is designed to work in concert with WXPython, not abstract it away entirely. However, for this guide, no WXPython knowledge is required. We'll walk you through the few pieces you need to know as they come up. 

>If you want to learn more about WXPython, checkout these resources for great overviews
>  * [official docs](https://docs.wxpython.org/Overviews.html)
>  * [Mouse vs Python blog](http://www.blog.pythonlibrary.org/)


## Elements and Rendering 

```
from rewx import create_element
from rewx.components import Frame 

create_element(Frame, {'title': 'My first element'})
```

At the heart of re-wx is the `Element`. This is just a piece of data that describes the **type** of thing you want in the UI, and the **properties** you want it to have (refered to as "props" from here on out). An Element is just a python map, and `create_element` is just a convenience function for generating it. Here's what the example above evaluates to:

```python
{
    'type': Frame, 
    'props': {'title': 'My First Element', children: []}
}
```

You build applications in re-wx by building trees of these elements. Here's an example which would display a bit of text in the UI like this. 

<p align="center">
  <img src="https://github.com/chriskiehl/re-wx-images/raw/images/screenshots/hello-world.png" align=center >
</p>


```
from rewx import create_element
from rewx.components import Frame, StaticText

create_element(Frame, {'title': 'My Cool Application', 'show': True}, children=[
  create_element(StaticText, {'label': 'Howdy, cool person!'})
])
```

Together, these elements make up the fancily titled "virtualdom," or, more like "virtual_frame_" in our case. We specify our application in plain ol' boring data, and let re-wx handle the heavy lifting on getting things turned into a GUI. 

The core thing to notice is that at no point do we have to deal with how these collections of Elements get transformed into GUI elements, or how their instances are managed, or any of the low-level details you generally have to deal with when using Desktop GUI frameworks. re-wx is all about creating applications using simple functions (and Componets, which we'll get to below) that take data as input and return data as output. 

Now, the question is how we get from our collections of Elements, to a live bunch of UI widgets. That's where rendering comes in. 


## WSX 

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


## Rendering 

Rendering handles all of the business involved in turning your tree of Elements into actual WX widgets. You'll find the `render` function in the main `rewx` module. 

```
from rewx import render
```

Render takes two arguments: The **Element** tree you want turned into UI widgets, and the **parent** to which these widgets should be attached. 

```python
render(create_element(Frame, {'title': 'Render demo'}), None)
```

Parent is any `wx.Object` **_or_** `None` if the top-level type in your Element tree is a `Frame`. Understanding **Parent** means understanding a bit of WXPython proper, but practically speaking, there are just two rules: 

If the root type in your re-wx element is a `Frame`, they you pass `None` to `parent`, otherwise, pass whichever `wx.Object` you'd like your elements to be rooted under. 

Option 1: rendering a top-level frame
```python
elements = create_element(Frame, {'title': 'Render demo'})
my_wx_instance = render(elements, None)
```

Option 2: rendering onto an already existing wx.Object

```python
frame = wx.Frame(None) 
elements = create_element(StaticText, {'label': 'Example'})
# everything in `elements` will be rooted under `frame` 
my_wx_instance = render(elements, frame)
```

the output of the render is a wx.Object which matches the `type` specified at the root of your element tree. Meaning, even though you've specified your application as plain data, after rendering, you've got a fully ready-to-go instance of a WX object. This can be used just like any other WX object, because it _is_ a WX object. It's because of this that re-wx is 100% compatible with existing WXPython codebases! 


## Creating reusable Elements

The humble function will be your main tool for managing reusability and clarity throughout your application. You can wrap up a group of related elements in a function and then use that function _just like you would any other Element_. 

```python 
# this is a plain ol' function that takes props 
# and returns an Element
def ConfigLine(props): 
    return wsx(
        [Block, {'orient': wx.HORIZONTAL},
          [TextCtrl, {...}],
          [Button, {...}]]
    )
```

```python
def control_panel(props): 
   return wsx(
       [Block, {'orient': wx.VERTICAL}, 
         [StaticText, {'label': 'Config Options'}],
         
         [ConfigLine, {some_props_here}],
         [ConfigLine, {some_props_here}],
         [ConfigLine, {some_props_here}]]
   )
```



## Components 

Components let you create reusable bits of code just like functions, but they have one additional super power: the can store and manage state. 

You create components by declaring a class that inherits from `rewx.Component`. The most basic Component just includes a `render` method. 

```python 
from rewx import Component 
from rewx.components import Frame, StaticText 

class MyComponent(Component):
   def render(props): 
       return wsx(
           [Block, {}, 
             [StaticText, {'label': f"Hello {props['name']!"}]]
       )
```

You use them just like you would any other Type in re-wx, by turning them into an Element:

```python
create_element(MyComponent, {'name': 'My component'})
```

Because Components are turned into Elements like everything else, you can freely mix and match between re-wx provided components and your own custom ones to build larger units of functionality: 

```python
wsx(
  [Block, {}, 
    [MyComponent, {'name': 'My Component'}],
    [StaticText, {'label': 'Howdy'}]]
)
```

You can even use Components inside of other Components! 

```python
from rewx import Component, wsx, render, create_element
from rewx.components import StaticText, Frame

class ComponentA(Component):
    def render(self):
        return wsx([StaticText, {'label': self.props['message']}])

class ComponentB(Component):
    def render(self):
        return wsx(
          [Frame, {'title': 'Composin Components', 'show': True},
            [ComponentA, {'message': 'I am rendered inside of Component B! Neat!'}]]
```

**Accessing Props**

Just like all the things we've seen so far, Components are use `props` to do useful things. You access them from the component instance via `self.props`. 

**Props are Immutable and Read-Only**

Component `props` should never be updated directly by your code. Meaning, doing something like `self.props['my_value'] = 10` is an **error**. The Componet itself will handle updating the props in response to changes in the rest of the app. This means that all of your code should be pure functions which take data as input and return data as output. re-wx handles all the updating behind the scenes. 


## Components and state

Components are how you manage state in re-wx. They could be as simple as something which keeps track of a counter or act as the central heart of your entire application. 

To show how all this works, we're going to walk through creating a simple, reusable clock component. This Component will display the current time, updated each second, wherever we put it in our application. 

You add state to a Component by overridding the Component's `__init__` method 

```
class Clock(Component): 
    def __init__(self, props): 
        super().__init__(props)  # don't forget this line!
        self.state = {} # you're state here
    
    def render(self):
        ...
```

>Note that the call to `super()` is _required_. Don't forget it! 

Just like `props`, your `state` can contain anything you want. Any valid Python map will work! Since we're building a clock, we'll store the current time in our state. 

```python
from datetime import datetime

class Clock(Component): 
    def __init__(self, props): 
        super().__init__(props) 
        # New! our state now holds the current time 
        self.state = {
            current_time: datetime.now()
        } 
    
    def render(self):
        ...
```

Now that we've defined some state, we can reference it any of the methods we define on our class by accessing `self.state`. Let's now update the `render` function to show this on the screen. 


```python
class Clock(Component): 
    def __init__(self, props): 
        super().__init__(props) 
        self.state = {
            current_time: datetime.now()
        } 
    
    # new!    
    def render(self):
        return wsx([StaticText, {'label': str(self.state['current_time'])}])
```

Just like `props` we can reference state directly in `render` in order to display it. However the default string formatting of Python's datetime object isn't very clock-like -- actually, it doesn't show any time info at all! Let's add a helper method to make the formatting more inline with what we expect. 

```python
class Clock(Component): 
    def __init__(self, props): 
        super().__init__(props) 
        self.state = {
            current_time: datetime.now()
        } 
    # new! 
    def format_time(self): 
        """Formats the datetime as the more clock-y hh:mm:ss"""
        return self.state['current_time'].strftime('%I:%M:%S')
        
    def render(self):
        # updated!
        return wsx([StaticText, {'label': self.format_time()}])
```

Check it out! We can reference state in any of the methods we define in our class! Here we setup a little helper which reads the current state, and transforms it into something more presentable for display in the UI. We then used that helper in our `render` method. 

So far so good, but our clock isn't much of a clock yet. It just sits there displaying whatver time it received on its first render. To fix this, we'll learn how to update state. 

**Updating state:** 

Your tool for updating Component state is the method `self.set_state()`. It takes the whatever the next state should be. Before we teach our clock to keep time on its own, let's introduce a button which will update the current time. This'll let us see `set_state` in action as well as a quick tour of event handling. 

> Important note: just like `props`, a component's `state` should be treated as an immutable, read-only value. It should _never_ be updated directly by modifying it it in place (e.g. `self.state['my_value'] = 'foo'`). re-wx is blind to these binds of mutations and will not know that it needs to re-render the changes. Always use `set_state` when you need to update your state!  


```
class Clock(Component): 
    def __init__(self, props): 
        super().__init__(props) 
        self.state = {
            current_time: datetime.now()
        } 
    ...
    # new!
    def update_time(self, event): 
        self.set_state({'current_time': datetime.now()})
    
    def render(self):
        return wsx(
          # new!
          [Block, {'orient': wx.HORIZONTAL},
            [StaticText, {'label': self.format_time()}],
            [Button, {'label': 'Update', 'on_click': self.update_time)
```

Here we added our button to `render` and set its `on_click` handler to a method we defined on our component called `update_time`. Now, whenever we click the button, `update_time` will get invoked, which calls `set_state` with the new state we're defining. re-wx is listening for these state changes and kicks off a `render` in response, thus causing our time display to be updated. This pattern is the core of how you'll build applications in re-wx. You only have to deal with declaring how things fit together and how state changes in response to event, and re-wx handles all the rest. 

Now, let's finish making this clock a proper clock. We want to start the clock as soon as it's available in UI. To do that, we have to talk about Life Cycle Methods 

## Component lifecycle methods

Very often, you'll want to take some action when a component is added to the GUI. In re-wx, we call this event _mounting_, and Component has a special hook method for this event called `component_did_mount()`. You can override this method in your class to handle any one-time initialization actions that you want to take place in the UI. 

It's important to understand the difference between the Component's _initialization_ and when the wx.Object is actually _mounted_ onto a Window. Initialization is what happens when your `__init__` method is called by re-wx. It is where you setup your state and any instance variables you may want. The key thing here is that _no WX widgets have been created at the time of initialization_. So, for instance, if you tried to access any part of the wx.Window or call `set_state`, you'd get an Exception thrown due the UI not yet being available. Conversey, _mounting_ is when all of the wx.Objects you've defined at actually attached to the `wx.Window`. This happens _after initialization_. It is at this point that the UI can be interacted with, [Ref](#Refs) are available, and everything is ready to rock. 

Sticking with our Clock example, we want to start a [`wx.Timer`](https://wxpython.org/Phoenix/docs/html/wx.Timer.html) and tie it to our update method so that the Clock actually keeps the current time automatically. Becuase we want these updates to be applied to the UI, we want to kick off this timer after _mounting_ not during _initialization_. As such, we'll define our timer inside of `component_did_mount`! 


```python 
class Clock(Component): 
    def __init__(self, props): 
        super().__init__(props) 
        # new! 
        self.timer = None
        self.state = {
            current_time: datetime.now()
        } 
    # new! 
    def component_did_mount():
        self.timer = wx.Timer()
        self.timer.Notify = self.update_time
        self.timer.Start(milliseconds=1000)
    
    def update_time(self, event): 
        self.set_state({'current_time': datetime.now()})
    
    def render(self):
        return wsx(
          # new!
          [Block, {'orient': wx.HORIZONTAL},
            [StaticText, {'label': self.format_time()}],
            [Button, {'label': 'Update', 'on_click': self.update_time)
```

That's it! Now when the component gets mounted onto the wx Window, we'll kick off a timer which updates the clock's display every second. 

At a high level, that's all there is to Components. With Elements, Functions, and Components under our belt, we've got all the tools we need to build advanced applications using re-wx! 


## Running re-wx Applications

There are three things you need to start any WxPyton application:

1. A `wx.App` instance
2. A toplevel `wx.Frame`
3. The `MainLoop`

The wx.App instance must be created before anything else. This is just a quirk of WxPython. It uses the creation of the App to instantiate a lot of platform dependent things. So, it's just a bit of boilerplate we need to keep WX happy. 

```python
import wx 

if __name__ == '__main__':
    app = wx.App()
```

Next you'll need a top-level `Frame`. They're a special type in WX and what we generally associate with the main window when we're using an application. This can either come from re-wx as part of rendering your elements, or can optionally be created separately if you're integrating with existing code. 

```python
import wx 
from rewx import render, wsx
from rewx.components import Frame, StaticText

if __name__ == '__main__':
    app = wx.App()
    my_element = wsx(
      [Frame, {'title': 'My Cool Application', 'show': True},
        [StaticText, {'label': 'Howdy, cool person!'}]]
    )
    frame = render(my_element, None) 
```

The last step in the process is kicking off the app's `MainLoop`. This is what gives WXPython control of the main thread of execution which it uses to launch the GUI and display your Frame. 

```python
import wx 
from rewx import render, wsx
from rewx.components import Frame, StaticText

if __name__ == '__main__':
    app = wx.App()
    my_element = wsx(
      [Frame, {'title': 'My Cool Application', 'show': True},
        [StaticText, {'label': 'Howdy, cool person!'}]]
    )
    frame = render(my_element, None) 
    app.MainLoop()
```

That's it! If you copy/paste the above into your editor, you'll be the proud owner of a Hello World application. 


