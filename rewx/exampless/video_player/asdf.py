from __future__ import print_function
import wx
import wx.media
import os

from rewx2 import Component, wsx
from rewx import components as c


class VideoPlayer(Component):
    def __init__(self, props):
        super().__init__(props)

    def on_load(self, event):
        pass

    def render(self):
        return wsx(
            [c.Block, {},
             [c.MediaCtrl, {'backend': wx.media.MEDIABACKEND_DIRECTSHOW,
                            'on_load': self.on_load}]]
        )


class StaticText(wx.StaticText):
    """
    A StaticText that only updates the label if it has changed, to
    help reduce potential flicker since these controls would be
    updated very frequently otherwise.
    """
    def SetLabel(self, label):

        if label != self.GetLabel():
            wx.StaticText.SetLabel(self, label)

#----------------------------------------------------------------------

class TestPanel(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent, -1,
                          style=wx.TAB_TRAVERSAL|wx.CLIP_CHILDREN)
        # Create some controls
        try:
            self.mc = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER,
                                         szBackend=wx.media.MEDIABACKEND_DIRECTSHOW
                                         #szBackend=wx.media.MEDIABACKEND_QUICKTIME
                                         #szBackend=wx.media.MEDIABACKEND_WMP10

                                         )
        except NotImplementedError:
            self.Destroy()
            raise
        # print(dir(self.mc))
        self.video_size = parent.GetSize()
        self.Bind(wx.media.EVT_MEDIA_LOADED, self.OnMediaLoaded)

        loadButton = wx.Button(self, -1, "Load File")
        self.Bind(wx.EVT_BUTTON, self.OnLoadFile, loadButton)
        playButton = wx.Button(self, -1, "Play")

        self.Bind(wx.EVT_BUTTON, self.OnPlay, playButton)
        self.playBtn = playButton

        pauseButton = wx.Button(self, -1, "Pause")
        self.Bind(wx.EVT_BUTTON, self.OnPause, pauseButton)
        stopButton = wx.Button(self, -1, "Stop")
        self.Bind(wx.EVT_BUTTON, self.OnStop, stopButton)
        self.slider = wx.Slider(self, -1, 0, 0, 12)
        self.slider.SetMinSize((self.video_size[0]-15, -1))
        self.Bind(wx.EVT_SLIDER, self.OnSeek, self.slider)
        self.st_size = StaticText(self, -1, size=(100,-1))
        self.st_len  = StaticText(self, -1, size=(100,-1))
        self.st_pos  = StaticText(self, -1, size=(100,-1))
        self.st_file = StaticText(self, -1, ".mid .mp3 .wav .au .avi .mpg", size=(200,-1))
        Bsizer = wx.BoxSizer(wx.VERTICAL)
        Lsizer = wx.BoxSizer(wx.HORIZONTAL)
        Lsizer.Add(loadButton, 0, wx.ALL, 5)
        Lsizer.Add(self.st_file, 0, wx.ALL, 5)
        Bsizer.Add(Lsizer)
        Bsizer.Add(self.mc, 1, wx.ALL, 5) # for .avi .mpg video files
        Bsizer.Add(self.slider)
        bsizer = wx.BoxSizer(wx.HORIZONTAL)
        bsizer.Add(playButton, 0, wx.ALL, 5)
        bsizer.Add(pauseButton, 0, wx.ALL, 5)
        bsizer.Add(stopButton, 0, wx.ALL, 5)
        Bsizer.Add(bsizer)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.st_size, 0, wx.ALL, 7)
        sizer.Add(self.st_len, 0, wx.ALL, 7)
        sizer.Add(self.st_pos, 0, wx.ALL, 7)
        Bsizer.Add(sizer)
        self.SetSizer(Bsizer)
        filename = "data/toy.mp4"
        if os.path.isfile(filename):
            wx.CallAfter(self.DoLoadFile, os.path.abspath(filename))
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer.Start(100)

    def OnLoadFile(self, evt):
        dlg = wx.FileDialog(self, message="Choose a media file",
                            defaultDir=os.getcwd(), defaultFile="",
                            style=wx.FD_OPEN | wx.FD_CHANGE_DIR )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.DoLoadFile(path)
        dlg.Destroy()

    def DoLoadFile(self, path):
        #self.playBtn.Disable()
        if not self.mc.Load(path):
            wx.MessageBox("Unable to load %s: Unsupported format?" % path,
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            folder, filename = os.path.split(path)
            self.st_file.SetLabel('%s' % filename)
            self.mc.SetInitialSize(self.video_size)
            self.GetSizer().Layout()
            self.slider.SetRange(0, self.mc.Length())

    def OnMediaLoaded(self, evt):
        self.playBtn.Enable()

    def OnPlay(self, evt):
        if not self.mc.Play():
            wx.MessageBox("Unable to Play media : Unsupported format?",
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mc.SetInitialSize(self.video_size)
            self.GetSizer().Layout()
            self.slider.SetRange(0, self.mc.Length())

    def OnPause(self, evt):
        self.mc.Pause()

    def OnStop(self, evt):
        self.mc.Stop()

    def OnSeek(self, evt):
        offset = self.slider.GetValue()
        self.mc.Seek(offset)

    def OnTimer(self, evt):
        offset = self.mc.Tell()
        self.slider.SetValue(offset)
        self.st_size.SetLabel('size: %s' % self.mc.Length())
        self.st_len.SetLabel('length: %d seconds' % (self.mc.Length()/1000))
        self.st_pos.SetLabel('position: %d' % offset)

    def ShutdownDemo(self):
        self.timer.Stop()
        del self.timer

app = wx.App(0)
frame = wx.Frame(None, size=(640, 480))
panel = TestPanel(frame)
frame.Show()
app.MainLoop()