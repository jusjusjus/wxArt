
import wx
import pysftp
import os
import threading
from .PasswordQuery import PasswordQuery
import wxArt_server


class ArtistManager(object):

    _sftp_server   = 'newton'
    _sftp_username = 'jschwab'
    _sftp_args     = (_sftp_server,)
    _sftp_kwargs   = dict(username=_sftp_username, password='')
    _server_path   = wxArt_server.__file__

    _remote_filenames = ['dummy']

    _pb_max = 5
    _pb_style = wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME

    _pwd_title = "Password for %s on %s" % (_sftp_username, _sftp_server)

    def __init__(self, parent):
        self.parent = parent
        self.query_password()


    def set_paths(self, content_path, style_path, network_path):
        self.content_path = content_path
        self.style_path   = style_path
        self.network_path = network_path


    def upload_files(self, files):

        uploaded_files = 0

        try:
            self.connection = pysftp.Connection(*self._sftp_args, **self._sftp_kwargs)
    
            for filename in files:
                if os.path.exists(filename):
                    self.connection.put( filename )
                    uploaded_files += 1
    
            self.connection.close()

        except:
            pass
        
        return uploaded_files


    def download_files(self):   # files are self._remote_filenames

        self.connection = pysftp.Connection(*self._sftp_args, **self._sftp_kwargs)

        for filename in self._remote_filenames:
            self.connection.get( filename )

        self.connection.close()


    def issue_command(self, command):
        self.connection = pysftp.Connection(*self._sftp_args, **self._sftp_kwargs)
        response = self.connection.execute(' '.join(command))  # command should return a list of files.
        self.connection.close()
        self.finished = True


    def construct_command(self):
        command = ['python', 'wxArt_server.py']
        return command


    def run(self):

        command = self.construct_command()

        self.worker    = threading.Thread(name='worker', target=self.issue_command, args=(command,))

        self.upload_files([self.content_path, self.style_path, self.network_path]) # Upload the files to newton.
        self.worker.start() # self.issue_command(command)

        dialog = wx.ProgressDialog("Berechnungsfortschritt", "Noch zu verbleibende Zeit", self._pb_max, style=self._pb_style)
        keepGoing = (True, False)
        self.finished = False
        count = 0

        while keepGoing[0] and not self.finished and count < self._pb_max:
            wx.Sleep(1) # sleep for 1 second.
            keepGoing = dialog.Update(count)
            count += 1

        self.connection.close() # This kills the worker, the connection and the remote process.
        dialog.Destroy()

        # Now we can gather the results.
        self.download_files()


    def query_password(self):

        if not os.path.exists(self._server_path):
            wx.MessageBox("Something went terribly wrong.")
            return
        
        while True:
            dialog = PasswordQuery(None, size=wx.Size(300, 50), title=self._pwd_title)
            dialog.ShowModal()

            self._sftp_kwargs["password"] = dialog.password
            
            # The server file has to be uploaded anyway.
            if self.upload_files([self._server_path]) > 0:   # Returns number of successfully uploaded files.
                return
