<p align="center">
  <img src="https://github.com/chriskiehl/re-wx-images/raw/images/logo/rewx.png"> 
</p>

A library for building modern declarative desktop applications in WX.

 * declarative: 
 * Component based -  
 * complete interop with the rest of your WX codebase - re-wx doesn't require you to change anything about your current codebase to start using it. Just create a component, attach it to an existing set of WX widgets, and off you go! 
 

This is an implementation of React's ideas _on top_ of WX. 


What if instead of subclassing, we could write declarative, data-driven code? 

```python
def application(): 
    return \ 
      [block, 
        [input1, {'on_input': handle_input, 'placeholder': 'Enter something!'}],
        [button, {'on_click': handler}]]
```


Rationale: 

Development in WX blows.Wrappers around C++ classes. Evertything requires subclassing a low-level plumbing code 


```python
class MyPanel(wx.Panel): 
    def __init__(self, parent, *args, **kwargs):
        super(MyPanel, self).__init__(parent, *args, **kwargs)
        self.sizers = ... 
        self.widgets = ... 
        self.foo == ... 
```  

# tradeoffs:

Practicality is favored over purity of abstraction. Meaning, you'll mix-match WXPython code + re-wx code as needed. A good example of this is for transient dialogs (confirming actions, getting user selectsions, etc..). In React land, you'd traditionally have a modal in your core markup, and then conditionally toggle its visibility via state. Here we'd just use the dialog directly rather than embedding it in the markup and handling its lifecycle via `is_open` style state flags. This is practical to do because, unlike React in Javascript, Python can block in place without affecting the main UI thread. Which allows writing 
straight forward in-line Dialog code.  

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

