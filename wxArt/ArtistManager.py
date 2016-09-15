
import wx
import pysftp
import os
import threading


class ArtistManager(object):

    _sftp_args   = ('newton',)
    _sftp_kwargs = dict(username='jschwab', password='')

    _remote_filenames = ['dummy']

    _pb_max = 5
    _pb_style = wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME

    def __init__(self, parent, content_path, style_path, network_path):

        self.parent       = parent
        self.content_path = content_path
        self.style_path   = style_path
        self.network_path = network_path


    def upload_files(self):

        self.connection = pysftp.Connection(*self._sftp_args, **self._sftp_kwargs)

        for filename in [self.content_path, self.style_path, self.network_path]:
            if os.path.exists(filename):
                self.connection.put( filename )

        self.connection.close()


    def download_files(self):   # files are self._remote_filenames

        self.connection = pysftp.Connection(*self._sftp_args, **self._sftp_kwargs)

        for filename in self._remote_filenames:
            self.connection.get( filename )

        self.connection.close()


    def issue_command(self, command):
        self.connection = pysftp.Connection(*self._sftp_args, **self._sftp_kwargs)
        response = self.connection.execute(' '.join(command))  # command should return a list of files.
        self.connection.close()
        print response
        self.finished = True


    def construct_command(self):
        command = ['python', 'wxArt_server.py']
        return command


    def run(self):

        command = self.construct_command()

        self.worker    = threading.Thread(name='worker', target=self.issue_command, args=(command,))

        self.upload_files() # Upload the files to newton.
        self.worker.start() # self.issue_command(command)

        dialog = wx.ProgressDialog("Berechnungsfortschritt", "Noch zu verbleibende Zeit", self._pb_max, style=self._pb_style)
        keepGoing = (True, False)
        self.finished = False
        count = 0

        while keepGoing[0] and not self.finished and count < self._pb_max:
            wx.Sleep(1) # sleep for 1 second.
            keepGoing = dialog.Update(count)
            print keepGoing
            count += 1

        self.connection.close() # This kills the worker, the connection and the remote process.
        dialog.Destroy()

        # Now we can gather the results.
        self.download_files()
