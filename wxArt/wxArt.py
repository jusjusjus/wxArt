#!/usr/env python
# ==============================================================================
# app.py
#
# Purpose:
# define the app that hosts the application frame
#
# ==============================================================================
#
import wx
from .Frame import Frame

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# % App Class
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class wxArt(wx.App):

    default_kwargs = dict(debug = False,
                          fps   = 20)

    def __init__(self, *args, **kwargs):
        '''
        steal constructor from parent class
        necessary???
        '''
        for att in self.default_kwargs.keys():
            if kwargs.has_key(att):
                setattr(self, att, kwargs.pop(att))
            else:
                setattr(self, att, self.default_kwargs[att])

        super(wxArt, self).__init__(*args, **kwargs)


    def OnInit(self):
        '''
        makes frame, gets called on init
        '''
        self.frame = Frame(None, size=wx.Size(1500, 800), title='wxArt', debug=self.debug, fps=self.fps)
        self.frame.Show()
        return True

    def OnExitApp(self, evt):
        self.frame.Close(True)
