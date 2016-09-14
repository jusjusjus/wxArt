#!/usr/env python
# ==============================================================================
# test_imagebutton.py
#
# Purpose:
# test and figure out how this pos works
# FIRST QUESTION: Why does this not work
#
# ==============================================================================
#
import numpy as np
import scipy as sp
import matplotlib
import pylab as pl
import sys
import wx

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# % ImageButton class
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# simple load images into wx.BitmapButtons
# no fixed size, as simple as possible
class ImageButton(wx.BitmapButton):

    def __init__(self, image_path, *args, **kwargs):
        super(ImageButton, self).__init__(*args, **kwargs)  # parent-class needs to be initialized
        # overwrite __init__ of BitmapButton

        # define image as an inner bitmap (redundant)
        self.image_path = image_path
        self.image = wx.Image(image_path,wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        # initial load
        self.load_image(image_path)

    def load_image(self, image_path):
        '''load image at path and set bitmap to image'''
        self.image = wx.Image(self.image_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        print type(self.image)
        self.SetBitmap(self.image)


if __name__=="__main__":
    app=wx.App()
    frame = wx.Frame(None)  # A frame is needed to show something.
    test=ImageButton('../resources/default_artist.png', frame)
    
    sizer = wx.BoxSizer(wx.VERTICAL) # The frame needs a sizer to organize the size of its items.
    frame.SetSizer(sizer)       # Set the sizer for the frame

    sizer.Add(test, wx.EXPAND)   # Add the Imagebutton to the sizer.

    frame.Show()                # show the frame

    app.MainLoop()              # start the control loop.
