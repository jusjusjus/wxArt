#!/usr/env python
# ==============================================================================
# image.py
#
# Purpose:
# define the ImageButton class, a class for wx.BitmapButtons
# with simple image change
#
# ==============================================================================
#
import os
import wx
from .ArtistManager import ArtistManager

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# % Image class
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class Image(wx.StaticBitmap):

    _defaultImage_path = os.path.dirname(__file__) + "/../resources/default_picture.jpg"

    _max  = ArtistManager._pb_max-1    # = len(_remote_filenames)-1

    def __init__(self, parent, *args, **kwargs):
        super(Image, self).__init__(parent, *args, **kwargs)

        # Initial load.  In here, self.path_to_image is set, which is used later
        # to send the pictures to the server for processing.  One should take
        # care that this path is always set correctly.
        self.load_image(self._defaultImage_path)

        slider_vsizer = self.slider_vsizer = wx.BoxSizer(wx.VERTICAL)
        slider = self.slider = wx.Slider(parent, -1, 2, 0, self._max, wx.DefaultPosition, (250, -1), style=wx.SL_AUTOTICKS)
        slider_label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        slider_min_label = wx.StaticText(parent, -1, "Content")
        slider_mid_label = wx.StaticText(parent, -1, "<===>")
        slider_max_label = wx.StaticText(parent, -1, "Style")
        slider_label_sizer.Add(slider_min_label, 0, wx.EXPAND, 0)
        slider_label_sizer.Add(wx.StaticText(parent, -1, ""), 1, wx.EXPAND, 0)
        slider_label_sizer.Add(slider_mid_label, 0, wx.EXPAND, 0)
        slider_label_sizer.Add(wx.StaticText(parent, -1, ""), 1, wx.EXPAND, 0)
        slider_label_sizer.Add(slider_max_label, 0, wx.EXPAND, 0)
        # add actual slider and slider labels to slider
        slider_vsizer.Add(slider, 0, wx.EXPAND, 0)
        slider_vsizer.Add(slider_label_sizer, 0, wx.EXPAND, 0)

        parent.Bind(wx.EVT_SLIDER, self.OnSlider, slider)


    def load_image(self, image_path):
        self.path_to_image = image_path
        bitmap = wx.Image(image_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.SetBitmap(bitmap)


    def get_path_to_image(self):
        return self.path_to_image


    def image_fit(self):
        # get size
        width, height = self.GetSize()

        # load image and get aspect ratio
        image_path = self.get_path_to_image()
        image = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
        Iwidth, Iheight = image.GetSize()
        aspect_ratio = float(Iwidth)/Iheight

        # compute possible sizes
        dummy_height = float(width)/aspect_ratio
        dummy_width = height*aspect_ratio

        # choose size that fits
        if width<dummy_width:
            image = image.Rescale(width, dummy_height, wx.IMAGE_QUALITY_HIGH)
        else:
            image = image.Rescale(dummy_width, height, wx.IMAGE_QUALITY_HIGH)
        bitmap = image.ConvertToBitmap()
        self.SetBitmap(bitmap)
        self.Refresh()


    def OnSlider(self, evt):
        pic_number = self.slider.GetValue()

        filename = ArtistManager._filenames[pic_number]

        if os.path.exists(filename):
            self.load_image( filename )
            self.image_fit()


