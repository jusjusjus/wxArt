import wx

class Frame(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(Frame, self).__init__(*args, **kwargs)
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)


        txt = wx.TextCtrl(self, -1)
        txt.SetHint("Enter some text")
        main_sizer.Add(txt, 1, wx.ALL | wx.EXPAND, 10)


        bitmap = wx.Image( "./resources/default_artist.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        button_sizer.Add(wx.Button(self, -1, "OK"), 0, wx.ALL, 10)
        button_sizer.Add(wx.BitmapButton(self, -1, bitmap), 1, wx.EXPAND | wx.ALL, 10)

        main_sizer.Add(button_sizer, 0, wx.EXPAND)

        self.SetSizerAndFit(main_sizer)


app = wx.App()

frame = Frame(None)
frame.Show()
app.MainLoop()
