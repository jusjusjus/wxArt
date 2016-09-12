
import wx
import wx.lib.agw.aui as aui
import os
from .image import Image

class frame(wx.Frame):

    default_stylefile   = os.path.dirname(__file__) + "/../resources/default_artist.png"
    default_contentfile = os.path.dirname(__file__) + "/../resources/default_avatar.png"
    default_picturefile = os.path.dirname(__file__) + "/../resources/default_picture.jpg"
    max_pane = 200
    min_pane = 40

    def __init__(self, *args, **kwargs):
        super(frame, self).__init__(*args, **kwargs)

        # auiManager to manage the two windows.
        manager = self.manager = aui.AuiManager(self)

        main_pane    = self.main_pane    = aui.AuiPaneInfo().CloseButton(False).PaneBorder(False).CaptionVisible(False).Center().Resizable()
        network_pane = self.network_pane = aui.AuiPaneInfo().CloseButton(False).PaneBorder(False).CaptionVisible(True).Left().Caption("Netzwerk Struktur").Resizable()

        main_panel    = self.main_panel    = wx.Panel(self, -1, size=wx.Size(-1, -1), style=wx.NO_BORDER)
        network_panel = self.network_panel = wx.Panel(self, -1, size=wx.Size(self.min_pane, -1), style=wx.NO_BORDER)   # todo
        network_panel.SetBackgroundColour(wx.WHITE)

        manager.AddPane(main_panel,    main_pane) 
        manager.AddPane(network_panel, network_pane) 
        manager.Update()

        # construct the main panel.
        win_size = self.GetClientSize()
        
        input_width = int(0.4 * win_size[0])
        input_pic_height = int(0.5* (win_size[1]-30))
        output_width =win_size[0] - input_width
        output_pic_height = int(0.9* win_size[1])

        main_hsizer = wx.BoxSizer(wx.HORIZONTAL)
        input_vsizer = wx.BoxSizer(wx.VERTICAL)
        output_vsizer = wx.BoxSizer(wx.VERTICAL)
        label_sizer = wx.BoxSizer(wx.HORIZONTAL)

        main_panel.SetSizer(main_hsizer) 
        main_hsizer.Add(input_vsizer, wx.EXPAND)
        main_hsizer.Add(output_vsizer, wx.EXPAND)

        # Place the three images 
        style_image   = self.style_image   = Image(self.default_stylefile,   wx.Size(input_width, input_pic_height), main_panel, -1)
        content_image = self.content_image = Image(self.default_contentfile, wx.Size(input_width, input_pic_height), main_panel, -1)
        button = self.button = wx.Button(main_panel, -1, "Jetzt malen!")

        input_vsizer.Add(style_image, wx.EXPAND)
        input_vsizer.Add(content_image, wx.EXPAND)
        input_vsizer.Add(button)

        # Place the output picture and slider
        picture_image = self.picture_image = Image(self.default_picturefile, wx.Size(output_width, output_pic_height), main_panel, -1)
        slider = self.slider = wx.Slider(main_panel, -1, maxValue=7, size=wx.Size(output_width, -1))
        email_field = wx.TextCtrl(main_panel, -1, size=wx.Size(output_width, -1))
        email_field.SetHint("Bitte geben Sie Ihre e-mail Adresse zum erhalten des Bildes")

        label_sizer.Add(wx.StaticText(main_panel, -1, "Stil"), wx.ALIGN_LEFT)
        label_sizer.AddSpacer(output_width-100)
        label_sizer.Add(wx.StaticText(main_panel, -1, "Inhalt"), wx.ALIGN_RIGHT)

        output_vsizer.Add(picture_image, wx.EXPAND)
        output_vsizer.Add(slider, wx.EXPAND)
        output_vsizer.Add(label_sizer, wx.EXPAND)
        output_vsizer.Add(email_field)

        # Get network architecture to the left and right.
        self.Bind(wx.EVT_BUTTON, self.load_style, style_image)
        self.Bind(wx.EVT_BUTTON, self.load_content, content_image)
        self.Bind(wx.EVT_BUTTON, self.save_picture, picture_image)

        network_panel.Bind(wx.EVT_ENTER_WINDOW, self.hide_show_pane)
        network_panel.Bind(wx.EVT_LEAVE_WINDOW, self.hide_show_pane)


    def hide_show_pane(self, event):

        if event.GetEventType() == wx.EVT_ENTER_WINDOW.typeId:
            new_size = self.max_pane
        else:
            new_size = self.min_pane

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
