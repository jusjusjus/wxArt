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
        height, width = cam_frame.shape[:2]
        self.bmp = wx.BitmapFromBuffer(width, height, cam_frame) # buffer for bitmap

        # link bitmap with image on buffer
        self.SetBitmap(self.bmp)

        # start timer to control redraw
        self.timer = wx.Timer(self)
        self.timer.Start(1000./fps)

        # bindings to redraw
        # self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextCam_Frame)
        self.video_on = True

        self.Bind(wx.EVT_BUTTON, self.halt_start_video, self)

    # def OnPaint(self, evt):
    #     '''
    #     when frame is painted, repaint button
    #     necessary???
    #     I thought repaint is controlled from outside
    #     does work without this method
    #     '''
    #     dc = wx.BufferedPaintDC(self)
    #     dc.DrawBitmap(self.bmp, 0, 0)

    def NextCam_Frame(self, event):
        '''
        when time is right get new snapshot from camera
        and update the bitmap
        '''
        ret, cam_frame = self.capture.read()
        if ret:
            cam_frame = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(cam_frame)
            self.Refresh()


    def halt_start_video(self, event):

        if self.video_on == True:
            self.timer.Stop()
            self.video_on = False

        else:
            self.timer.Start()
            self.video_on = True


    def FitBitmap(self):
        '''
        TODO
        does not work properly...
        '''
        image = wx.ImageFromBitmap(self.bmp_dummy)
        Bwidth, Bheight = self.GetClientSize()
        print Bwidth, Bheight
        image = image.Scale(Bwidth, Bheight)
        return wx.BitmapFromImage(image)


