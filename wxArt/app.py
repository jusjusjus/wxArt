
import wx 
from .frame import frame


class App(wx.App):

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)


    def OnInit(self):
        self.frame = frame(None, size=wx.Size(800, 600))
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.OnExitApp,  fileMenu.Append(wx.ID_EXIT, "&Quit Hypnox\tCtrl-Q"))
        menuBar.Append(fileMenu, "&File")
        self.frame.SetMenuBar(menuBar)
        self.frame.Show()
        return True
    

    def OnExitApp(self, evt):
        self.frame.Close(True)
