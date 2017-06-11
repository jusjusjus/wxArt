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
import subprocess
from .Camera import Camera

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# % AnmiatedDisplay
# In this class self.path_to_image refers to the currently loaded
# Image, which can be a .jpg, .png, but also a .gif object.  Everytime
# self.path_to_image is updated, the previous filename is stored in
# self.path_history.
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



class AnimatedDisplay(wx.animate.GIFAnimationCtrl):

    _input_frame_base = Camera._frame_base  # = 'frame'
    _output_frame_base = './large_'+_input_frame_base  # = 'large_frame'
    _gif_path = _output_frame_base+'s.gif'  # ='large_frames.gif'
    _defaultImage_path = os.path.dirname(__file__) + "/../resources/default_picture.jpg"

    def __init__(self, *args, **kwargs):

        if not kwargs.has_key('filename'):
            kwargs['filename'] = self._defaultImage_path

        super(AnimatedDisplay, self).__init__(*args, **kwargs)

        # AnimatedDisplay stores a history of files that have been loaded, and
        # to which one can return if they still exist.
        self.path_history = []
        self.history_position = -1


        # Initial load.  In here, self.path_to_image is set, which is used later
        # to send the pictures to the server for processing.  One should take
        # care that this path is always set correctly.
        self.load_image(self._defaultImage_path)     # Load default image without calling child routines!


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
        print "image height and width:", height, width
        if width<dummy_width:
            image = image.Rescale(width, dummy_height, wx.IMAGE_QUALITY_HIGH)
        else:
            image = image.Rescale(dummy_width, height, wx.IMAGE_QUALITY_HIGH)
        bitmap = image.ConvertToBitmap()
        self.SetInactiveBitmap(bitmap)
        self.GetParent().Layout()
        self.Refresh()


    def revert(self, event):
        # Jump back one step in history
        if self.history_position == 0:
            return
        self.history_position -= 1
        self.path_to_image = self.path_history[self.history_position]
        self.do_load_image()


    def forward(self, event):
        # Jump back one step in history
        if self.history_position == len(self.path_history)-1:
            return
        self.history_position += 1
        self.path_to_image = self.path_history[self.history_position]
        self.do_load_image()


    def load_image(self, image_path):
        self.path_to_image = image_path
        self.path_history.append(self.path_to_image)
        self.history_position = len(self.path_history)-1    # move to end of history
        self.do_load_image()


    def do_load_image(self):
        bitmap = wx.Image(self.path_to_image, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.SetBitmap(bitmap)


    def load_video(self, fps):

        for frame in self.get_frames_to_process():
            self.fit_and_save(frame[0], frame[1])

        self.path_to_image = self.merge_to_gif(fps=fps)  # Merge all artworks into one movie.
        self.path_history.append( self.path_to_image )
        self.history_position = len(self.path_history)-1    # move to end of history

        self.do_load_video(fps)


    def do_load_video(self, fps):
        self.LoadFile(self.path_to_image)
        self.GetParent().Layout()
        self.Play()


    def SetBitmap(self, bitmap):
        self.Stop()
        self.SetInactiveBitmap(bitmap)
        self.image_fit()


    # Methods for gif-creation
    def get_frames_to_process(self):
        possible_in_frames  = (self._input_frame_base+'_%03i.jpg' % (i) for i in xrange(1000))
        possible_out_frames = (self._output_frame_base+'_%03i.jpg' % (i) for i in xrange(1000))

        frames = []
        for fi, fo in zip(possible_in_frames, possible_out_frames):
            # if input file exists, append filenames.
            if os.path.exists(fi):
                frames.append([fi, fo])
            else:
                break

        return frames


    def merge_to_gif(self, fps):

        gif_path = self._gif_path

        try:
            subprocess.call(['rm', self._gif_path])
        except (WindowsError, IOError):
            if os.path.exists(self._gif_path):
                os.remove(self._gif_path)
        subprocess.call(['ffmpeg', '-f', 'image2',
                         '-framerate', str(fps),
                         '-i', self._output_frame_base+'_%03d.jpg',
                         gif_path])

        return gif_path


    def fit_and_save(self, infile, outfile):
        width, height = self.GetSize()

        # load image and get aspect ratio
        image = wx.Image(infile, wx.BITMAP_TYPE_ANY)
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

        image.SaveFile(outfile, wx.BITMAP_TYPE_JPEG)


    def save_image(self, outfile):
        path = self.get_path_to_image()
        image = wx.Image(path, wx.BITMAP_TYPE_ANY)
        image.SaveFile(outfile, wx.BITMAP_TYPE_JPEG)



