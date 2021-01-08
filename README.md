<p align="center">
  <img src="https://github.com/chriskiehl/re-wx-images/raw/images/logo/rewx.png"> 
</p>

A library for building modern declarative desktop applications in WX.

 * Declarative: 
 * Component based -  
 * complete interop with the rest of your WX codebase - re-wx doesn't require you to change anything about your current codebase to start using it. Just create a component, attach it to an existing set of WX widgets, and off you go! 
 
re-wx is an implementation of React's ideas _on top_ of WX Python. It allows you to decouple your state and logic from your UI, and declaratively state blah blah blah. 



```python

def controls(props): 
    return wsx(
        [Block, {'orient': wx.HORIZONTAL}, 
          [Button, {'on_click': props['on_start'], 'label': 'Ok'}],
          [Button, {'on_click': props['on_cancel'], 'label': 'Cancel'}]]
    )
```

### virtualframe and diffing 

### WSX

`create_element` is the fundamental building block of all of re-wx. However, its verbose and can make viewing your UIs structure at a glance difficult as it gets lost in a sea of method call noise. As an alternative, you can use list to represent elements in a syntax which loosely resembles HTML (if you squint a lot). 

```python
def my_component(props): 
   return wsx(
     [Block, {'orient': wx.VERTICAL}, 
       [Block, {'orient': wx.HORIZONTAL}, 
         [StaticText, {'label': 'Foobar'}],
         [Button, {'label': 'Submit', 'on_click': props['on_click']}]]]
   )
```

the `wsx` call will transform that into the equivalent form 

```python
def my_component(props): 
   return create_element(Block, {'orient': wx.VERTICAL}, children=[
       create_element(Block, {'orient': wx.HORIZONTAL}, children=[
           create_element(StaticText, {'label': 'Foobar'})
           create_element(StaticText, {'label': 'Submit', 'on_click': props['on_click']})
       ])
       
   ])
```

Two paths to the same place, so you can use whichever one feels most natural. 



WX Widgets currently managed by re-wx. 



Head on over to the Getting Started guide to find out more. 

Rationale: 

Development in WX blows.Wrappers around C++ classes. Evertything requires subclassing a low-level plumbing code 

<h2 align="center">Quick Demos!</h2>

<img src="https://github.com/chriskiehl/re-wx-images/raw/images/screenshots/hello-world.png" align=right >

**Starting Small.** You can assemble applications with re-wx using the humble function. This takes data and returns data. re-wx handles all the lifting required to build the WX instances. 

```python
from app import basicapp
from rewx import create_element
from rewx.components import StaticText

def say_hello(props):
    return create_element(StaticText, {'label': f'Howdy, {props["name"]}!'})

if __name__ == '__main__':
    element = create_element(say_hello, {'name': 'cool person'})
    basicapp(element, title='My Cool Application!', debug=True)
```  


### A Stateful component 

<img src="https://github.com/chriskiehl/re-wx-images/raw/images/screenshots/clock.png" align=right >

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

## Philosophy

re-wx is not trying to be an general purpose abstraction over multiple backend UI kits. It's lofty goals begin and end with it being a way of making writing native UIs in WX easier. As such, it doesn't need reconcilers, or generic transactions, or any of the React bloat. re-wx entire codebase is just a handful of files < 1k lines of code, and could be understood in an afternoon.  

Practicality is favored over purity of abstraction. Meaning, you'll mix-match WXPython code + re-wx code as needed. A good example of this is for transient dialogs (confirming actions, getting user selectsions, etc..). In React land, you'd traditionally have a modal in your core markup, and then conditionally toggle its visibility via state. However, in re-wx, you'll just use the dialog directly rather than embedding it in the markup and handling its lifecycle via `is_open` style state flags. This is practical to do because, unlike React in Javascript, WX handles managing the UI thread thus allowing us to block in place without any negative effects. Which allows writing straight forward in-line Dialog code.  

```python
def handle_choose_dir(self, event): 
    dlg = wx.DirDialog(None)
    if dlg.Show() == wx.ID_OK:
        self.setState({'directory': dlg.GetPath()})
``` 

Events: re-wx does no event wrapping. The normal WX events are used. 

It's not trying to be an opaque framework hiding away the internal details of WX. It's very much designed to operate on-top of and in concert with WX. 

# compromises

It's not a true one-way data flow for certain components. For instance, in WX, ComboBoxes only produce events _after_ it's internally updated its state. 

Another example is TextCtrl. EVT_TEXT is fired _after_ the textctrl has been updated. There's EVT_CHAR, however, it's so low level that handling it would require essentailly reimplementing the TextCtrl itself from scratch. 

However, in practice, this tends to not matter much. You can still update the control in rsponse to the event, which generally happens fast enough that the transient state isn't noticed by the user (if shown on the screen at all!)


More caveats: 

Only the most common attributes are currently managed by declarative props (basically, most of what falls under `wx.Control`). Specifics such as `InsertionPoint`s in TextCtrls are considered out of scope for rewx. `Ref`s act as a handy escape-hatch for any lower level API needs .

More Caveats: 

The prefab RadioGroup cannot have its number of options changed after creation. So, jiggling the `choices` will have no effect. The good news is that RadioGroup is largely just a convenience class, if you need to dynamically vary the options, you can simulate the RadioGroup via 

TODO
```python
class MyRadioGroup(Component): 
    def render(self):
        return wsx(
            ['borderbox', {} ]
        )


``` 



# Current state of the world: 

Implementation notes: 

Reconciliation doesn't have many performance focused smarts at this point. It only looks at the current props to decide what to do, and thus blanket unsets/resets values every time, as opposed to a more nuanced approach which diff'd the prev/current props and conditionally updated only those pieces which need changes. However, so far, with moderately sized UIs, this naieve approach hasn't produced any notable performance issues. This may change in the future.  
 


# Important Note!

Lambdas inside of lists: 

```python
[{
    'attrs': {
        'on_click': lambda x: self.doThing(dynamicThing) 
    }
} for dynamicThing in self.state['things']]
```

This is wrong! See: [link to python docs ]

Use `callwith`
```python
[{
    'attrs': {
        'on_click': callwith(self.doThing, dynamicThing) 
    }
} for dynamicThing in self.state['things']]

```

