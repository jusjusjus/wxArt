#!/usr/env python
# ==============================================================================
# camerabutton.py
#
# Purpose:
# define CameraButton class that is a button and video frame
#
# ==============================================================================
#
import wx
#from .imagebutton import ImageButton
import cv2
import tempfile

from skimage import io
import os



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# % CameraButton class
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class Camera(wx.StaticBitmap):

    _frame_base = 'frame'
    _countdown_path = os.path.dirname(__file__) + "/../resources/countdown/"
    _defaultImage_path = os.path.dirname(__file__) + "/../resources/default_picture.jpg"
    default_kwargs = dict(debug = False,
                          fps   = 20)

    def __init__(self, *args, **kwargs):

        for att in self.default_kwargs.keys():
            if kwargs.has_key(att):
                setattr(self, att, kwargs.pop(att))
            else:
                setattr(self, att, self.default_kwargs[att])

        super(Camera, self).__init__(*args, **kwargs)

        #assert self.fps < 30, 'CameraButton: frame rate too high, too high...'

        # generate capture object and start reading camera buffer
        self.InitBitmapBuffer()

        # start timer to control redraw
        self.timer = wx.Timer(self)
        self.timer.Start(1000./self.fps)

        # Timer that does recording.
        self.rectimer = wx.Timer(self)

        # bindings to redraw
        self.Bind(wx.EVT_TIMER, self.show_next_frame, self.timer)
        self.video_on  = True                        # Flag indicate video state.
        self.recording = False

        # set value for path_to_image 
        self.path_to_image = "./content.jpg"


    def show_next_frame(self, event):
        '''
        when time is right get new snapshot from camera
        and update the bitmap
        '''
        ret, cam_frame = self.capture.read()
        if cam_frame is None:
            ret, cam_frame = self.capture_stub()

        if ret:
            cam_frame = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2RGB)
            self.CopyFromBuffer(cam_frame)
            self.GetParent().Layout()
        

    def record_next_frame(self, event):
        '''When time is right get new snapshot from camera
        and update the bitmap'''
        ret, cam_frame = self.capture.read()
        if cam_frame is None:
            ret, cam_frame = self.capture_stub()
        if ret:
            cam_frame = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2RGB)
            self.CopyFromBuffer(cam_frame)

            self.record_image(filename=self._frame_base+"_{:03d}.jpg".format(self.i_rec))
            self.i_rec += 1
            self.GetParent().Layout()


    def InitBitmapBuffer(self):
        # Creates cam2bmp - bitmap buffer, that can quickly read out the camera.
        # To make full use of this one needs to find a better mechanism for plotting
        # later, because self.bmp is re-created every time.  However, I don't know
        # how to real with the raw bitmaps.

        self.capture = cv2.VideoCapture(0)
        ret, cam_frame = self.capture.read()
        if cam_frame is None:
            ret, cam_frame = self.capture_stub()
    
        if self.debug:
            print cam_frame
    
        cam_frame = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2RGB)

        height, width = cam_frame.shape[:2]
        self.cam2bmp = wx.BitmapFromBuffer(width, height, cam_frame) # buffer for bitmap
        self.SetBitmap(self.cam2bmp)


    def CopyFromBuffer(self, cam_frame):
        self.cam2bmp.CopyFromBuffer(cam_frame[:, ::-1, :].flatten())
        self.Refresh()


    def record_image(self, filename=None):
        
        if filename == None:
            filename = self.path_to_image

        image = self.cam2bmp.ConvertToImage().Mirror()      # cam2bmp is already mirrored.  That's why we call it again.
        image.SaveFile(filename, wx.BITMAP_TYPE_JPEG)


    def countdown(self, evt):   # runs down the countdown.

        self.count -= 1
        if self.count > 0:  # While countdown is running..
            path = self._countdown_path+"mnist_%i.jpg" % (self.count)
            self.image_fit(path)
            self.GetParent().Layout()
    
        else: # Coundown over -> start the recording..
            # Stop the countdown timer
            self.timer.Stop()
            self.Unbind(wx.EVT_TIMER, self.timer)

            # Set the recording vars..
            self.recording = True
            self.i_rec = 0  # frame index for the recording

                # delete previously recorded frames
            possible_frames = (self._frame_base+'_%03i.jpg' % (i) for i in xrange(1000))
            for f in possible_frames:
                if os.path.exists(f):
                    os.remove(f)

            # Bind the video timer
            self.Bind(wx.EVT_TIMER, self.record_next_frame, self.timer)
            self.show_next_frame(None) # To empty the backed-up buffer
            self.show_next_frame(None) # To empty the backed-up buffer
            self.show_next_frame(None) # To empty the backed-up buffer
            self.show_next_frame(None) # To empty the backed-up buffer
            self.SetBitmap(self.cam2bmp)

            # Start the video/recording timer
            self.timer.Start(1000./self.fps)
            self.rectimer.Start(1000. * 2.) # Record 2 seconds of video.


    def take_snapchat(self, evt):
        # Unbind the video timer
        self.timer.Stop()
        self.Unbind(wx.EVT_TIMER, self.timer)

        # Bind the countdown timer
        self.count = 4
        self.Bind(wx.EVT_TIMER, self.countdown, self.timer)
        self.timer.Start(750.) # Record 2 seconds of video.

        path = self._countdown_path+"mnist_%i.jpg" % (self.count)
        self.image_fit(path)
        self.GetParent().Layout()


    def video_off(self, evt):
        self.recording = False
        self.rectimer.Stop()
        self.Unbind(wx.EVT_TIMER, self.timer)
        self.Bind(wx.EVT_TIMER, self.show_next_frame, self.timer)
        if not evt == None: evt.Skip()


    def get_path_to_image(self): # Takes a snapshot before ..
        return self.path_to_image


    def load_image(self, image_path):
        self.path_to_image = image_path
        bitmap = wx.Image(image_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.SetBitmap(bitmap)


    def image_fit(self, image_path=None):

        if image_path == None:
            image_path = self.get_path_to_image()

        # get size
        width, height = self.GetSize()

        # load image and get aspect ratio
        image = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
        Iwidth, Iheight = image.GetSize()
        aspect_ratio = float(Iwidth)/Iheight

        # compute possible sizes
        dummy_height = float(width)/aspect_ratio
        dummy_width = height*aspect_ratio

        # choose size that fits
        if width<dummy_width:
            image = image.Rescale(width,dummy_height,wx.IMAGE_QUALITY_HIGH)
        else:
            image = image.Rescale(dummy_width,height,wx.IMAGE_QUALITY_HIGH)
        bitmap = image.ConvertToBitmap()
        self.SetBitmap(bitmap)


    @staticmethod
    def capture_stub():
        """Stub to give images without camera.
    
        :return:
        """
        image = io.imread(os.path.abspath(os.path.dirname(__file__) + "/../resources/default_picture.jpg"))
        return 0, image[:, :, [2, 1, 0]]
