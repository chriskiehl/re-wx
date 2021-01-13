# Main Concepts

* [Elements](#Elements)
* [WSX](#WSX)
* [Rendering](#Rendering)
* [Running a re-wx App](#running-a-re-wx-app)
* [Rendering](#Rendering)


### Knowledge Level Assumptions 

re-wx is designed to work in concert with WXPython, not abstract it away entirely. However, for this guide, no WXPython knowledge is required. We'll walk you through the few pieces you need to know as they come up. 

>If you want to learn more about WXPython, checkout these resources for great overviews
>  * [official docs](https://docs.wxpython.org/Overviews.html)
>  * [Mouse vs Python blog](http://www.blog.pythonlibrary.org/)


## Hello World 

<p align="center">
  <img src="https://github.com/chriskiehl/re-wx-images/raw/images/screenshots/hello-world.png" align=center >
</p>

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

Components are how you create independent, reusable, stateful entities in re-wx. 

Components are just like Elements. Meaning, they have a `type` and take `props`. However, they have a few additional super powers.  

, but they have a few additional super powers. They act as independent, reusable pieces of UI code, and one additional super power: they store and manage state across renders. 


You create components by declaring a class that inherits from `rewx.Component`. 

```python 
from rewx import Component 
from rewx.components import Frame, StaticText 

class MyComponent(Component):
   def render(props): 
       return wsx(
           [Block, {}, 
             [StaticText, {'label': 'Hello Components!'}]]
       )
```

**Component philosophy:** 

Fewer are preferable to many. State is the hardest thing to manage in programming. 


Components are how you manage state in re-wx. They could be as simple as adding a counter to a text input, or act as the heart of your entire application. 


## Running the App

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


