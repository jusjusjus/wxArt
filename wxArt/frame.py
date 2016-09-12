
import wx
import os
from .image import Image

class frame(wx.Frame):

    default_stylefile   = os.path.dirname(__file__) + "/../resources/default_artist.png"
    default_contentfile = os.path.dirname(__file__) + "/../resources/default_avatar.png"
    default_picturefile = os.path.dirname(__file__) + "/../resources/default_picture.jpg"

    def __init__(self, *args, **kwargs):
        super(frame, self).__init__(*args, **kwargs)

        win_size = self.GetClientSize()
        slider_size = wx.Size(win_size[0]-100, -1)
        picture_size = wx.Size(win_size[0]/3, win_size[1]-50)


        main_vsizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(main_vsizer) 

        image_hsizer = wx.BoxSizer(wx.HORIZONTAL)
        main_vsizer.Add(image_hsizer, wx.EXPAND)

        slider_hsizer = wx.BoxSizer(wx.HORIZONTAL)
        main_vsizer.Add(slider_hsizer, wx.EXPAND)

        # Place the three images 
        style_image   = self.style_image   = Image(self.default_stylefile,   picture_size, self, -1)
        content_image = self.content_image = Image(self.default_contentfile, picture_size, self, -1)
        picture_image = self.picture_image = Image(self.default_picturefile, picture_size, self, -1)

        image_hsizer.Add(style_image, wx.EXPAND)
        image_hsizer.Add(picture_image, wx.EXPAND)
        image_hsizer.Add(content_image, wx.EXPAND)

        # Place a slider and button
        slider = self.slider = wx.Slider(self, -1, maxValue=10000, size=slider_size)
        button = self.button = wx.Button(self, -1, "Jetzt malen!")

        slider_hsizer.Add(slider, wx.EXPAND)
        slider_hsizer.Add(button, wx.EXPAND)

        # Get network architecture to the left and right.
        self.Bind(wx.EVT_BUTTON, self.load_style, style_image)
        self.Bind(wx.EVT_BUTTON, self.load_content, content_image)
        self.Bind(wx.EVT_BUTTON, self.save_picture, picture_image)


    def load_style(self, event):

        dialog = wx.FileDialog(self,
                               "Stilschema laden...",
                               "",
                               "",
                               "Image files (*.png)|*.png",
                               wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_OK:
            self.style_image.load_image(dialog.GetPath())


    def load_content(self, event):

        dialog = wx.FileDialog(self,
                               "Inhalt laden...",
                               "",
                               "",
                               "Image files (*.png)|*.png",
                               wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_OK:
            self.content_image.load_image(dialog.GetPath())


    def save_picture(self, event):

        dialog = wx.FileDialog(self,
                               "Resultat speichern...",
                               "",
                               "",
                               "Image files (*.png)|*.png",
                               wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if dialog.ShowModal() == wx.ID_OK:
            self.content_image.save_image(dialog.GetPath())
