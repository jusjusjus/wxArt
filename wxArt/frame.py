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
import os
from .image import Image
from .EmailCtrl import EmailCtrl

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# % frame class
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
# draw the main window of the application
class frame(wx.Frame):
    #
    # ~~~~~ constant members ~~~~~
    _default_stylefile   = os.path.dirname(__file__) + "/../resources/default_artist.png"
    _default_contentfile = os.path.dirname(__file__) + "/../resources/default_avatar.png"
    _default_picturefile = os.path.dirname(__file__) + "/../resources/default_picture.jpg"
    _max_pane = 200
    _min_pane = 0

    def __init__(self, *args, **kwargs):
        super(frame, self).__init__(*args, **kwargs)
        self.Maximize(True)

        #
        # ~~~~~ auiManager ~~~~~
        # manage two panels
        # left: network panel
        # right: main panel
        manager = self.manager = aui.AuiManager(self)

        # panes
        main_pane    = self.main_pane    = aui.AuiPaneInfo().CloseButton(False).PaneBorder(False).CaptionVisible(False).Center().Resizable()
        network_pane = self.network_pane = aui.AuiPaneInfo().CloseButton(False).PaneBorder(False).CaptionVisible(True).Left().Caption("Netzwerk Struktur").Resizable()

        # panels
        main_panel    = self.main_panel    = wx.Panel(self, -1, size=wx.Size(-1, -1), style=wx.NO_BORDER)
        network_panel = self.network_panel = wx.Panel(self, -1, size=wx.Size(self._min_pane, -1), style=wx.NO_BORDER)   # todo
        network_panel.SetBackgroundColour(wx.WHITE)

        # add panels to manager
        manager.AddPane(main_panel,    main_pane)
        manager.AddPane(network_panel, network_pane)
        manager.Update()

        #
        # ~~~~~ main panel (right) ~~~~~
        # hosts two sizer
        # left: input
        # right: output
        main_hsizer = wx.BoxSizer(wx.HORIZONTAL)
        input_vsizer = wx.BoxSizer(wx.VERTICAL)
        output_vsizer = wx.BoxSizer(wx.VERTICAL)

        main_panel.SetSizer(main_hsizer)
        main_hsizer.Add(input_vsizer, 1, wx.EXPAND | wx.ALL, 10)
        main_hsizer.Add(output_vsizer, 1, wx.EXPAND | wx.ALL, 10)

        #
        # ~~~~~ input sizer (left) ~~~~~
        # mange the user input
        # top: content (camera button)
        # bottom: style (image button)
        style_image   = self.style_image   = Image(self._default_stylefile,   wx.Size(0,0), main_panel, -1)
        content_image = self.content_image = Image(self._default_contentfile, wx.Size(0,0), main_panel, -1)
        button = self.button = wx.Button(main_panel, -1, "Jetzt malen!")

        input_vsizer.Add(style_image, 1, wx.EXPAND | wx.ALL, 10)
        input_vsizer.Add(content_image, 1, wx.EXPAND | wx.ALL, 10)
        input_vsizer.Add(button, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        #
        # ~~~~~ output sizer (right) ~~~~~
        # display the result of the content-style-merging
        # top: output image
        # middle: slider to change alpha value
        # bottom: email line, input email address and button to send mail
        picture_image = self.picture_image = Image(self._default_picturefile, wx.Size(0,0), main_panel, -1)

        # slider
        slider_vsizer=wx.BoxSizer(wx.VERTICAL)
        # actual slider
        slider = self.slider = wx.Slider(main_panel, -1, 4, 0, 4, wx.DefaultPosition, (250,-1), style=wx.SL_AUTOTICKS)
        # slider labels
        slider_label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        slider_min_label = wx.StaticText(main_panel,-1,"Style")
        slider_mid_label = wx.StaticText(main_panel,-1,"<===>")
        slider_max_label = wx.StaticText(main_panel,-1,"Content")
        slider_label_sizer.Add(slider_min_label, 0, wx.EXPAND, 0)
        slider_label_sizer.Add(wx.StaticText(main_panel, -1, ""), 1, wx.EXPAND, 0)
        slider_label_sizer.Add(slider_mid_label, 0, wx.EXPAND, 0)
        slider_label_sizer.Add(wx.StaticText(main_panel, -1, ""), 1, wx.EXPAND, 0)
        slider_label_sizer.Add(slider_max_label, 0, wx.EXPAND, 0)
        # add actual slider and slider labels to slider
        slider_vsizer.Add(slider,0,wx.EXPAND,0)
        slider_vsizer.Add(slider_label_sizer,0,wx.EXPAND,0)

        # email line
        email_sizer = wx.BoxSizer(wx.HORIZONTAL)
        email_field = EmailCtrl(main_panel, -1)
        email_field.SetHint(u'Für Erhalt des Bilder, bitte E-Mail-Adresse angeben.')
        email_button = wx.Button(main_panel,-1,"Senden")
        email_sizer.Add(email_field, 1, wx.EXPAND | wx.ALL, 10)
        email_sizer.Add(email_button, 0, wx.ALL, 10)

        output_vsizer.Add(picture_image, 1, wx.EXPAND | wx.ALL, 10)
        output_vsizer.Add(slider_vsizer, 0, wx.EXPAND | wx.ALL , 10)
        output_vsizer.Add(email_sizer, 0, wx.EXPAND | wx.ALL, 10)

        #
        # ~~~~~ bind events to functions ~~~~~
        # main panel
        self.Bind(wx.EVT_BUTTON, self.load_style, style_image)
        self.Bind(wx.EVT_BUTTON, self.load_content, content_image)
        self.Bind(wx.EVT_BUTTON, self.save_picture, picture_image)
        # network panel
        network_panel.Bind(wx.EVT_ENTER_WINDOW, self.hide_show_pane)
        network_panel.Bind(wx.EVT_LEAVE_WINDOW, self.hide_show_pane)

    #
    # ~~~~~ functions bound to events ~~~~~
    def hide_show_pane(self, event):
        '''
        hide and show panel depending on whether focused of not
        '''
        if event.GetEventType() == wx.EVT_ENTER_WINDOW.typeId:
            new_size = self._max_pane
        else:
            new_size = self._min_pane

        self.network_pane.MinSize(wx.Size(new_size, -1)).Fixed()
        self.manager.Update()


    def load_style(self, event):
        dialog = wx.FileDialog(self,
                               "Stilschema laden...",
                               "",
                               "",
                               "Image files (*.png)|*.png",
                               wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_OK:
            self.style_image.load_image(dialog.GetPath())


    def load_content(self, event):
        dialog = wx.FileDialog(self,
                               "Inhalt laden...",
                               "",
                               "",
                               "Image files (*.png)|*.png",
                               wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_OK:
            self.content_image.load_image(dialog.GetPath())


    def save_picture(self, event):
        dialog = wx.FileDialog(self,
                               "Resultat speichern...",
                               "",
                               "",
                               "Image files (*.png)|*.png",
                               wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if dialog.ShowModal() == wx.ID_OK:
            self.content_image.save_image(dialog.GetPath())
