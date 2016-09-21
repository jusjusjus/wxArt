
import wx


class PasswordQuery(wx.Dialog):

    def __init__(self, fields, *args, **kwargs):
        super(PasswordQuery, self).__init__(*args, **kwargs)

        self.input = dict()

        sizer = wx.GridSizer(cols=2)

        self.user = dict()

        for (field, default) in fields:
            label = wx.StaticText(self, label=field, size=wx.Size(200, -1))

            if field == 'password':
                input_widget = wx.TextCtrl(self, size=wx.Size(200, -1), style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)

            else:
                input_widget = wx.TextCtrl(self, size=wx.Size(200, -1), style=wx.TE_PROCESS_ENTER)

            input_widget.SetValue(str(default))
            self.user[field] = input_widget

            sizer.Add(label, 0,         wx.ALL | wx.CENTER | wx.EXPAND, 1)
            sizer.Add(input_widget, 0,  wx.ALL | wx.CENTER | wx.EXPAND, 1)

            self.Bind(wx.EVT_TEXT_ENTER, self.get_input, input_widget)


        self.SetSizer(sizer)

    
    
    def get_input(self, evt):

        for key in self.user:
            self.input[key] = self.user[key].GetValue()

        self.Show(False)
