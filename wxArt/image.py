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
import wx.animate

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# % Image class
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class Image(wx.animate.GIFAnimationCtrl):

    _defaultImage_path = os.path.dirname(__file__) + "/../resources/default_picture.jpg"

    def __init__(self, parent, *args, **kwargs):
        super(Image, self).__init__(parent, *args, **kwargs)

        # Initial load.  In here, self.path_to_image is set, which is used later
        # to send the pictures to the server for processing.  One should take
        # care that this path is always set correctly.
        Image.load_image(self, self._defaultImage_path)     # Load default image without calling child routines!


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
        self.SetInactiveBitmap(bitmap)
        self.Refresh()


    def load_image(self, image_path):
        self.path_to_image = image_path
        bitmap = wx.Image(image_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.SetInactiveBitmap(bitmap)


