#!/usr/env python
# -*- coding: utf-8 -*-
# ==============================================================================
# frame.py
#
# Purpose:
# specify frame class that generates frame of application
# most important application file
#
# ==============================================================================
#
import wx
import wx.lib.agw.aui as aui
import wx.animate
from .Artwork import Artwork
from .StyleButton import StyleButton
from .EmailCtrl import EmailCtrl
from .Camera import Camera
from .Postcard import Postcard
import subprocess


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# % Frame class
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
# draw the main window of the application
class Frame(wx.Frame):
    #
    # ~~~~~ constant members ~~~~~
    _max_pane = 200
    _min_pane = 0

    default_kwargs = dict(debug = False,
                          fps   = 20)

    def __init__(self, *args, **kwargs):

        for att in self.default_kwargs.keys():
            if kwargs.has_key(att):
                setattr(self, att, kwargs.pop(att))
            else:
                setattr(self, att, self.default_kwargs[att])

        super(Frame, self).__init__(*args, **kwargs)
        self.Maximize(True)

        # panels
        main_panel = self.main_panel = wx.Panel(self, -1, size=wx.Size(-1, -1), style=wx.NO_BORDER)

        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        menu_open = fileMenu.Append(wx.ID_OPEN, "Open File")
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)

        #
        # ~~~~~ main panel (right) ~~~~~
        # hosts two sizer
        # left: input
        # right: output
        main_hsizer = wx.BoxSizer(wx.HORIZONTAL)
        input_vsizer = wx.BoxSizer(wx.VERTICAL)
        output_vsizer = wx.BoxSizer(wx.VERTICAL)
        button_hsizer = wx.BoxSizer(wx.HORIZONTAL)

        main_panel.SetSizer(main_hsizer)
        main_hsizer.Add(input_vsizer, 2, wx.EXPAND | wx.ALL, 10)
        main_hsizer.Add(output_vsizer, 5, wx.EXPAND | wx.ALL, 10)

        #
        # ~~~~~ input sizer (left) ~~~~~
        # mange the user input
        # top: content (camera button)
        # bottom: style (image button)
        camera = self.camera = Camera(main_panel,-1, debug=self.debug, fps=self.fps)
        style_image   = self.style_image   = StyleButton(main_panel, -1)
        photo_button = self.photo_button   = wx.Button(main_panel, -1, "Fotografie")
        video_button = self.video_button   = wx.Button(main_panel, -1, "Aufnahme")
        paint_button = self.paint_button   = wx.Button(main_panel, -1, "kunstwerk malen")
        pcard_button = self.pcard_button   = wx.Button(main_panel, -1, "Postkarte erstellen")

        paint_button.Disable()
        pcard_button.Disable()

        input_vsizer.Add(camera, 1, wx.EXPAND | wx.ALL, 10)
        input_vsizer.Add(style_image, 1, wx.EXPAND | wx.ALL, 10)
        input_vsizer.Add(button_hsizer, 1, wx.EXPAND | wx.ALL, 10)
        button_hsizer.Add(photo_button, 1, wx.ALIGN_CENTER | wx.ALL, 10)
        button_hsizer.Add(video_button, 1, wx.ALIGN_CENTER | wx.ALL, 10)
        button_hsizer.Add(paint_button, 1, wx.ALIGN_CENTER | wx.ALL, 10)
        button_hsizer.Add(pcard_button, 1, wx.ALIGN_CENTER | wx.ALL, 10)

        #
        # ~~~~~ output sizer (right) ~~~~~
        # display the result of the content-style-merging
        # top: output image
        # middle: slider to change alpha value
        # bottom: email line, input email address and button to send mail
        artwork_image = self.artwork_image = Artwork(main_panel, -1)  # Image.slider_vsizer has to be set later!

        output_vsizer.Add(artwork_image, 1, wx.EXPAND | wx.ALL, 10)

        # EMAIL
        email_field = self.email_field = EmailCtrl(main_panel, -1)
        email_field.SetHint(u'Zum Verschicken des Bildes bitte eine E-Mail-Adresse angeben.')

        if email_field.IsEditable(): # Add the e-mail stuff only if available.
            email_button = wx.Button(main_panel, -1, "Senden")
            email_sizer = wx.BoxSizer(wx.HORIZONTAL)
            email_sizer.Add(email_field, 1, wx.EXPAND | wx.ALL, 10)
            email_sizer.Add(email_button, 0, wx.ALL, 10)
            self.Bind(wx.EVT_BUTTON,     self.send_as_email, email_button)  #
            self.Bind(wx.EVT_TEXT_ENTER, self.send_as_email, email_field)   # Redundancy.

            output_vsizer.Add(email_sizer, 0, wx.EXPAND | wx.ALL, 10)
        else: # Destroy!
            email_field.Destroy()


        #
        # ~~~~~ bind events to functions ~~~~~
        # main panel
        self.Bind(wx.EVT_BUTTON,     self.take_picture,   photo_button)
        self.Bind(wx.EVT_BUTTON,     self.issue_postcard,   pcard_button)

        self.Bind(wx.EVT_MENU, self.OnOpenFile, menu_open)

        self.Bind(wx.EVT_BUTTON,   camera.take_snapchat,       video_button)
        camera.Bind(wx.EVT_TIMER,  self.take_video,            camera.rectimer)

        self.Bind(wx.EVT_BUTTON,   self.convert_to_artwork,    paint_button)

        main_panel.Layout()


    def query_save(self):

        dialog = wx.MessageDialog(None, "Erlauben Sie uns Ihr Kunstwerk in unserer Zeitschrift zu benutzen?", "Erlaubniserteilung", wx.YES_NO)  # Change text to Ja/Nein
        answer = dialog.ShowModal()

        if answer == wx.ID_YES:
            self.artwork_image.arxiv()
            
        dialog.Destroy()
        #dialog should destroy right away, but doesn't.

    def send_as_email(self, event):

        if not self.email_field.IsEditable():
            wx.MessageBox("Unable to send as e-mail.")
            return

        # Gather attachment info.
        content_path = self.camera.get_path_to_image()
        style_path   = self.style_image.get_path_to_image()
        picture_path = self.artwork_image.get_path_to_image()

        self.query_save()   # This command issues a save-file to the artwork_image if the user allows us.

        attachments = [content_path,        # add path to content.
                       style_path,            # add path to style.
                       picture_path]        # add path to picture.

        # Issue e-mail-send command.
        self.email_field.send_email(attachments)


    def take_picture(self, event):
        # gether information
        self.paint_button.Enable()
        self.pcard_button.Enable()
        self.camera.record_image()
        content_path = self.camera.get_path_to_image()   # Get path to content.
        self.artwork_image.load_image(content_path)


    def take_video(self, event):
        self.paint_button.Enable()
        self.pcard_button.Disable()
        self.camera.video_off(None)
        self.artwork_image.load_video(fps = self.fps)


    def enable_paint(self, evt):
        self.paint_enable.Enable()


    def convert_to_artwork(self, event):
        style_path       = self.style_image.get_path_to_image()     # Get path to style.
        style_model_path = self.style_image.get_style_model()
        self.artwork_image.set_style(style_model_path)

        self.artwork_image.convert_to_artwork(fps = self.fps)


    def issue_postcard(self, event):
        pcard_operator = Postcard(self)
        pcard_operator.create()
        

    def OnOpenFile(self, event):
        self.paint_button.Enable()
        self.pcard_button.Enable()
        dialog = wx.FileDialog(self,
                               message="",
                               style=wx.FD_OPEN)

        if dialog.ShowModal() == wx.ID_OK:
            paths = dialog.GetPaths()
            for file in paths:
                self.camera.load_image(file)
                break

        dialog.Destroy()

