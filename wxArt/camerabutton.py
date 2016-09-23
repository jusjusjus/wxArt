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
from .imagebutton import ImageButton
import cv, cv2
import tempfile

from skimage import io
import os



def capture_stub():
    """Stub to give images without camera.

    :return:
    """
    image = io.imread(os.path.abspath(os.path.dirname(__file__) + "/../resources/selfie.jpg"))
    return 0, image[:, :, [2, 1, 0]]


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# % CameraButton class
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class CameraButton(ImageButton):

    default_kwargs = dict(debug = False,
                          fps   = 20)

    def __init__(self, *args, **kwargs):

        for att in self.default_kwargs.keys():
            if kwargs.has_key(att):
                setattr(self, att, kwargs.pop(att))
            else:
                setattr(self, att, self.default_kwargs[att])

        super(CameraButton, self).__init__(*args, **kwargs)

        #assert self.fps < 30, 'CameraButton: frame rate too high, too high...'

        # generate capture object and start reading camera buffer
        self.capture = cv2.VideoCapture(0)
        ret, cam_frame = self.capture.read()
        if cam_frame is None:
            ret, cam_frame = capture_stub()

        if self.debug:
            print cam_frame

        cam_frame = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2RGB)

        # make bitmap from buffer
        self.InitBitmapBuffer( cam_frame )

        # start timer to control redraw
        self.timer = wx.Timer(self)
        self.timer.Start(1000./self.fps)

        # bindings to redraw
        self.Bind(wx.EVT_TIMER, self.NextCam_Frame)
        self.video_on = True                        # Flag indicate video state.

        self.Bind(wx.EVT_BUTTON, self.halt_start_video, self)

        # set value for path_to_image 
        self.path_to_image = "./content.jpg"


    def NextCam_Frame(self, event):
        '''
        when time is right get new snapshot from camera
        and update the bitmap
        '''
        ret, cam_frame = self.capture.read()
        if cam_frame is None:
            ret, cam_frame = capture_stub()
        if ret:
            cam_frame = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2RGB)
            self.CopyFromBuffer(cam_frame)
            # self.Refresh() # unnecessary


    def InitBitmapBuffer(self, cam_frame):
        # Creates cam2bmp - bitmap buffer, that can quickly read out the camera.
        # To make full use of this one needs to find a better mechanism for plotting
        # later, because self.bmp is re-created every time.  However, I don't know
        # how to real with the raw bitmaps.
        height, width = cam_frame.shape[:2]
        self.cam2bmp = wx.BitmapFromBuffer(width, height, cam_frame) # buffer for bitmap
        self.SetBitmap(self.cam2bmp)


    def CopyFromBuffer(self, cam_frame):
        # The rescaling (2 lines down) is kind of funky:  it only increases in
        # size and it doesn't keep the aspect ratio intact.
        self.cam2bmp.CopyFromBuffer(cam_frame[:, ::-1, :].flatten())
        self.Refresh()


    def halt_start_video(self, event):

        if self.video_on == True:
            self.take_snapshot()
            self.video_on = False

        else:
            self.timer.Start()
            self.video_on = True


    def take_snapshot(self):
        self.timer.Stop()   # Stop timer.  Remember: last snapshot is still in cam2bmp.
        image = self.cam2bmp.ConvertToImage().Mirror()    # Don't mirror!
        image.SaveFile(self.path_to_image, wx.BITMAP_TYPE_JPEG)

    def get_path_to_image(self): # overwrite

        if self.video_on == True:           # forgot to turn it off.  Let's do it:
            self.halt_start_video( None )   # Trigger halt event.  Halting takes a snapshot.

        return super(CameraButton, self).get_path_to_image()   # Call mother function.


    def snapchat(self, duration=2., frame_rate=7):    # duration in seconds
        pass
