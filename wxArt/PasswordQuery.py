
import wx


class PasswordQuery(wx.Dialog):

    def __init__(self, *args, **kwargs):
        super(PasswordQuery, self).__init__(*args, **kwargs)

        self.password = ""

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, label="Enter Password")

        sizer.Add(label, 0, wx.ALL | wx.CENTER, 5)

        self.user = wx.TextCtrl(self, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)

        sizer.Add(self.user, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(sizer)

        self.Bind(wx.EVT_TEXT_ENTER, self.set_password, self.user)
    
    
    def set_password(self, evt):
        self.password = self.user.GetValue()
        self.Destroy()
