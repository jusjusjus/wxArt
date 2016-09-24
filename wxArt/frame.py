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
from .artwork import Artwork
from .stylebutton import StyleButton
from .EmailCtrl import EmailCtrl
from .camerabutton import CameraButton
from .styledialog import StyleDialog
from .postcard import Postcard
import subprocess


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# % frame class
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
# draw the main window of the application
class frame(wx.Frame):
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

        super(frame, self).__init__(*args, **kwargs)
        self.Maximize(True)

        #self.arts_manager = ArtistManager(self)

        #
        # ~~~~~ auiManager ~~~~~
        # manage two panels
        # left: network panel
        # right: main panel
        manager = self.manager = aui.AuiManager(self)

        # panes
        main_pane    = self.main_pane    = aui.AuiPaneInfo().CloseButton(False).PaneBorder(False).CaptionVisible(False).Center().Resizable()

        # panels
        main_panel    = self.main_panel    = wx.Panel(self, -1, size=wx.Size(-1, -1), style=wx.NO_BORDER)

        # add panels to manager
        manager.AddPane(main_panel,    main_pane)
        manager.Update()

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
        main_hsizer.Add(input_vsizer, 1, wx.EXPAND | wx.ALL, 10)
        main_hsizer.Add(output_vsizer, 1, wx.EXPAND | wx.ALL, 10)

        #
        # ~~~~~ input sizer (left) ~~~~~
        # mange the user input
        # top: content (camera button)
        # bottom: style (image button)
        content_image = self.content_image = CameraButton(main_panel,-1, debug=self.debug, fps=self.fps)
        style_image   = self.style_image   = StyleButton(main_panel, -1)
        paint_button = self.paint_button   = wx.Button(main_panel, -1, "Photo")
        video_button = self.video_button   = wx.Button(main_panel, -1, "Video")
        pcard_button = self.pcard_button   = wx.Button(main_panel, -1, "Postkarte")

        input_vsizer.Add(content_image, 1, wx.EXPAND | wx.ALL, 10)
        input_vsizer.Add(style_image, 1, wx.EXPAND | wx.ALL, 10)
        input_vsizer.Add(button_hsizer, 1, wx.EXPAND | wx.ALL, 10)
        button_hsizer.Add(paint_button, 1, wx.ALIGN_CENTER | wx.ALL, 10)
        button_hsizer.Add(video_button, 1, wx.ALIGN_CENTER | wx.ALL, 10)
        button_hsizer.Add(pcard_button, 1, wx.ALIGN_CENTER | wx.ALL, 10)

        #
        # ~~~~~ output sizer (right) ~~~~~
        # display the result of the content-style-merging
        # top: output image
        # middle: slider to change alpha value
        # bottom: email line, input email address and button to send mail
        artwork_image = self.artwork_image = Artwork(main_panel, -1)  # Image.slider_vsizer has to be set later!

        #artwork_gif = self.artwork_gif = wx.animate.GIFAnimationCtrl(main_panel, -1, "")  # Image.slider_vsizer has to be set later!
        #artwork_gif.Show(False)

        # email line
        email_sizer = wx.BoxSizer(wx.HORIZONTAL)
        email_field = self.email_field = EmailCtrl(main_panel, -1)
        email_field.SetHint(u'Zum Verschicken des Bildes bitte eine E-Mail-Adresse angeben.')
        email_button = wx.Button(main_panel,-1,"Senden")
        email_sizer.Add(email_field, 1, wx.EXPAND | wx.ALL, 10)
        email_sizer.Add(email_button, 0, wx.ALL, 10)

        output_vsizer.Add(artwork_image, 1, wx.EXPAND | wx.ALL, 10)
        #output_vsizer.Add(artwork_gif, 1, wx.EXPAND | wx.ALL, 10)
        output_vsizer.Add(email_sizer, 0, wx.EXPAND | wx.ALL, 10)

        #
        # ~~~~~ initialize style dialog ~~~~~
        self.styledlg = StyleDialog(self, -1, debug=self.debug)
        self.styledlg.current_path = self.style_image.get_path_to_image()

        #
        # ~~~~~ bind events to functions ~~~~~
        # main panel
        self.Bind(wx.EVT_BUTTON,     self.load_style,    style_image)
        self.Bind(wx.EVT_BUTTON,     self.issue_paint,   paint_button)
        self.Bind(wx.EVT_BUTTON,     self.issue_postcard,   pcard_button)
        self.Bind(wx.EVT_BUTTON,     self.send_as_email, email_button)  #
        self.Bind(wx.EVT_TEXT_ENTER, self.send_as_email, email_field)   # Redundancy.


        self.Bind(wx.EVT_BUTTON,          content_image.take_snapchat, video_button)
        content_image.Bind(wx.EVT_TIMER,  self.issue_video,            content_image.rectimer)

    #
    # ~~~~~ functions bound to events ~~~~~
    def load_style(self, event):
        self.styledlg.ShowModal()
        self.style_image.load_image(self.styledlg.current_path)
        self.style_image.image_fit()


    def send_as_email(self, event):

        if not self.email_field.IsEditable():
            wx.MessageBox("Unable to send as e-mail.")
            return

        # Gather attachment info.
        content_path = self.content_image.get_path_to_image()
        style_path   = self.style_image.get_path_to_image()
        picture_path = self.artwork_image.get_path_to_image()

        attachments = []
        attachments.append(content_path)        # add path to content.
        attachments.append(style_path)          # add path to style.
        attachments.append(picture_path)        # add path to picture.

        # Issue e-mail-send command.
        self.email_field.send_email(attachments)


    def issue_paint(self, event):
        # gether information
        content_path = self.content_image.get_path_to_image()   # Get path to content.
        style_path   = self.style_image.get_path_to_image()     # Get path to style.

        style_model_path = self.style_image.get_style_model()

        self.artwork_image.set_style(style_model_path)
        self.artwork_image.load_image(content_path)


    def issue_video(self, event):
        self.content_image.video_off(None)

        style_path       = self.style_image.get_path_to_image()     # Get path to style.
        style_model_path = self.style_image.get_style_model()

        self.artwork_image.set_style(style_model_path)
        self.artwork_image.load_images(fps=self.fps)

        # Send the information
        #self.arts_manager.set_paths(content_path, style_path)
        #self.arts_manager.run()


    def issue_postcard(self, event):
        pcard_operator = Postcard(self)
        pcard_operator.create()
