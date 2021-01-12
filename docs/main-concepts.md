# Main Concepts

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

At the heart of re-wx is the `Element`. This is just a piece of data that describes the **type** of thing you want in the UI, and the **properties** you want it to have (refered to as "props" from here on out). `create_element` is just a convenience function for generating a Python map. Here's what the example above evaluates to:

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


The magical thing to notice is that at no point do we have to deal with how these collections of Elements get transformed into GUI elements, or how their instances are managed, or any of the low-level details you generally have to deal with when using Desktop GUI frameworks.   


Components 


Rendering 

