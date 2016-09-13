#!/usr/env python
# ==============================================================================
# image.py
#
# Purpose:
# define the Image class, a class for wx.BitmapButtons
# with simple image change
#
# ==============================================================================
#
import wx

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# % Image class
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class Image(wx.BitmapButton):

    def __init__(self, defaultImage_path, picture_size, *args, **kwargs):
        super(Image, self).__init__(*args, size=picture_size, **kwargs)

        self.defaultImage_path = defaultImage_path
        self.picture_size = defaultImage_path

        # initial load
        self.load_image(self.defaultImage_path)


    def load_image(self, image_path):
        png = wx.Image(image_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.SetBitmap(png)
