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
from .frame import frame

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# % App Class
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class App(wx.App):

    def __init__(self, *args, **kwargs):
        '''
        steal constructor from parent class
        necessary???
        '''
        super(App, self).__init__(*args, **kwargs)

    def OnInit(self):
        '''
        makes frame, gets called on init
        '''
        self.frame = frame(None, size=wx.Size(1500, 800), title='wxArt')
        self.frame.Show()
        self.frame.email_field.query_password()
        return True

    def OnExitApp(self, evt):
        self.frame.Close(True)
