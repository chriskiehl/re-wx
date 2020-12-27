# re-wx
An experiment in bringing React(ish) style development to WXPython

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

Practicality is favored over purity of abstraction. Meaning, you'll mix-match WXPython code + re-wx code as needed. A good example of this is for transient dialogs (confirming actions, getting user selectsions, etc..). Here we'd just use the dialog directly rather than embedding it in the markup and handling its lifecycle via `is_open` style state flags. This is practical to do because, unlike React in Javascript, Python can block in place without affecting the main UI thread. Which allows writing 
straight forward in-line Dialog code.  

```python
def handle_choose_dir(self, event): 
    dlg = wx.DirDialog(None)
    if dlg.Show() == wx.ID_OK:
        self.setState({'directory': dlg.GetPath()})
``` 

Events: re-wx does no event wrapping. The normal WX events are used. 

# compromises

It's not a true one-way data flow for certain components. For instance, in WX, ComboBoxes only produce events _after_ it's internally updated its state. 

Another example is TextCtrl. EVT_TEXT is fired _after_ the textctrl has been updated. There's EVT_CHAR, however, it's so low level that handling it would require essentailly reimplementing the TextCtrl itself from scratch. 

However, in practice, this tends to not matter much. You can still update the control in rsponse to the event, which generally happens fast enough that the transient state isn't noticed by the user (if shown on the screen at all!)


 


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

