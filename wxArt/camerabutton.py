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
import cv, cv2

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# % CameraButton class
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class CameraButton(wx.BitmapButton):

    def __init__(self, fps, *args, **kwargs):
        super(CameraButton, self).__init__(*args, **kwargs)

        assert fps<=30, 'CameraButton: frame rate too high, too high...'

        # generate capture object and start reading camera buffer
        self.capture = cv2.VideoCapture(0)
        ret, cam_frame = self.capture.read()
        cam_frame = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2RGB)

        # make bitmap from buffer
        self.InitBitmapBuffer( cam_frame )

        # start timer to control redraw
        self.timer = wx.Timer(self)
        self.timer.Start(1000./fps)

        # bindings to redraw
        self.Bind(wx.EVT_TIMER, self.NextCam_Frame)
        self.video_on = True                        # Flag indicate video state.

        self.Bind(wx.EVT_BUTTON, self.halt_start_video, self)


    def NextCam_Frame(self, event):
        '''
        when time is right get new snapshot from camera
        and update the bitmap
        '''
        ret, cam_frame = self.capture.read()
        if ret:
            cam_frame = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2RGB)
            self.CopyFromBuffer(cam_frame)
            self.Refresh()


    def InitBitmapBuffer(self, cam_frame):
        # Creates cam2bmp - bitmap buffer, that can quickly read out the camera.
        # To make full use of this one needs to find a better mechanism for plotting
        # later, because self.bmp is re-created every time.  However, I don't know
        # how to real with the raw bitmaps.
        height, width = cam_frame.shape[:2]
        self.cam2bmp = wx.BitmapFromBuffer(width, height, cam_frame) # buffer for bitmap


    def CopyFromBuffer(self, cam_frame):
        # The rescaling (2 lines down) is kind of funky:  it only increases in
        # size and it doesn't keep the aspect ratio intact.
        self.cam2bmp.CopyFromBuffer(cam_frame)
        mirror_image = self.cam2bmp.ConvertToImage().Mirror()
        #width, height = self.GetClientSize()                   # defunkt
        #mirror_image = mirror_image.Scale(width, height)       # defunkt
        self.bmp = wx.BitmapFromImage( mirror_image )
        self.SetBitmap(self.bmp)


    def halt_start_video(self, event):

        if self.video_on == True:
            self.timer.Stop()
            self.video_on = False

        else:
            self.timer.Start()
            self.video_on = True


