
import wx

class frame(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(frame, self).__init__(*args, **kwargs)

        main_vsizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(main_vsizer) 

        image_hsizer = wx.BoxSizer(wx.HORIZONTAL)
        main_vsizer.Add(image_hsizer, wx.EXPAND)

        slider_hsizer = wx.BoxSizer(wx.HORIZONTAL)
        main_vsizer.Add(slider_hsizer, wx.EXPAND)

        # placeholders
        image_hsizer.Add(wx.StaticText(self, -1, "Style"), wx.EXPAND)
        image_hsizer.Add(wx.StaticText(self, -1, "Synthesis"), wx.EXPAND)
        image_hsizer.Add(wx.StaticText(self, -1, "Content"), wx.EXPAND)


        win_size = self.GetClientSize()

        slider = self.slider = wx.Slider(self, -1, maxValue=10000, size=wx.Size(win_size[0]-100, -1))
        button = self.button = wx.Button(self, -1, "Compute")

        slider_hsizer.Add(slider, wx.EXPAND)
        slider_hsizer.Add(button, wx.EXPAND)
