#!/usr/env python
# -*- coding: iso-8859-1 -*-
# ==============================================================================
# styledialog.py
#
# Purpose:
# define the StyleDialog class, that is responsible for style changes
#
# ==============================================================================
#
import wx
import wx.lib.agw.aui as aui
import os
from .ImageButton import ImageButton


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# % StyleDialog class
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class StyleDialog(wx.Dialog):
    _styledir = os.path.dirname(__file__) + '/../resources/styles'
    _buttonSize = (250,250)
    _ncolumns = 5
    def __init__(self,*args,**kwargs):
        
        if kwargs.has_key('debug'):
            self.debug = kwargs.pop('debug')
        else:
            self.debug = False

        super(StyleDialog,self).__init__(*args, **kwargs)

        self.SetTitle('Select Style')
        self.current_path = ""

        #
        # ~~~~~ load list of files and images ~~~~~
        # name, info, image
        self.file_dict = list()
        self.load_files()

        #
        # ~~~~~ panel and sizer ~~~~~
        # styles make centered dialog of three styles per row
        # manager = aui.AuiManager(self)
        panel = wx.Panel(self, -1, size=wx.Size(-1, -1), style = wx.NO_BORDER)
        panel.SetBackgroundColour(wx.WHITE)

        #
        # ~~~~~ construct and fill grid sizer ~~~~~
        # add buttons and info into vertical sizer
        # add vertical sizer into grid, rows=3
        grid = wx.GridBagSizer(hgap=1,vgap=1)
        panel.SetSizer(grid)
        for i in range(len(self.file_dict)):
            try:
                # generate sizer and image button
                vsizer = wx.BoxSizer(wx.VERTICAL)
                ibutton = ImageButton(panel,-1,size=self._buttonSize)
                # load image
                ibutton.load_image(self._styledir + '/' + self.file_dict[i]['name'])
                # fit image into button
                ibutton.image_fit()
                # add everything to sizer
                vsizer.Add(ibutton,1, wx.ALIGN_CENTER, 0)
                for info in self.file_dict[i]['info']:
                    vsizer.Add(wx.StaticText(panel,-1,info),0,wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_TOP,0)
                # add to grid
                pos = (i/self._ncolumns,i%self._ncolumns)
                grid.Add(vsizer, pos=pos)
                # BIND BUTTON
                # needs to be done here!!
                ibutton.Bind(wx.EVT_BUTTON, lambda evt, string=ibutton.get_path_to_image() : self.OnClick(evt, string))
            except:
                pass

            if self.debug == True: break

        # fit dialog around grid
        grid.Fit(self)

    def OnClick(self, event, string):
        '''
        change current path to path of clicked image path
        '''
        self.current_path = string
        self.Close()

    def load_files(self):
        '''
        load list of files and images
        files list of dicts:
        name (name of file)
        info (each info extracted from file)
            '-' separates info
            '_' translates to white space
        image
        generate file name list
        '''
        file_names = os.listdir(self._styledir) # file name list
        file_names.sort()
        # generate file info list
        file_info = list() # translate file names into infos
        for name in file_names:
            splitinfo = os.path.splitext(name)[0].split('-')
            for i in range(len(splitinfo)):
                splitinfo[i] = splitinfo[i].replace('_',' ')
            file_info.append(splitinfo)
        # generate file image list
        file_images = list()
        for name in file_names:
            image = wx.Image(self._styledir + '/' + name)
            file_images.append(image)
        # generate dict
        self.file_dict = list()
        keys=['name','info','image']
        for i in range(len(file_names)):
            values = [file_names[i],file_info[i],file_images[i]]
            dictionary = dict()
            for i in range(3):
                dictionary[keys[i]]=values[i]
            self.file_dict.append(dictionary)
