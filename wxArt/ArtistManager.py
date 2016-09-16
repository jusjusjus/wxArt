
import wx
import pysftp
import os
import threading
from .PasswordQuery import PasswordQuery
import wxArt_server
import numpy as np


class ArtistManager(object):

    _sftp_server   = 'newton'
    _sftp_username = 'jschwab'
    _sftp_args     = (_sftp_server,)
    _sftp_kwargs   = dict(username=_sftp_username, password='') # XXX
    _server_path   = wxArt_server.__file__.strip('c')   # because of the .pyc files

    _remote_filenames = wxArt_server.FIGUREPATHS
    _figuredir = './'
    _filenames = [ _figuredir + os.path.basename(filename)  for filename in _remote_filenames ]

    _pb_max = len(_remote_filenames)
    _pb_style = wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME

    _pwd_title = "Password for %s on %s" % (_sftp_username, _sftp_server)

    def __init__(self, parent):
        self.parent = parent
        self.query_password()


    def set_paths(self, content_path, style_path, network_path):
        self.content_path      = content_path
        self.style_path        = style_path
        self.remote_style_path = wxArt_server.STYLEDIR + os.path.basename(self.style_path)
        self.network_path      = network_path


    def upload_files(self, files, remote_dirs=None):

        if remote_dirs == None:
            remote_dirs = ['./'] * len(files)

        uploaded_files = 0

        try:
            self.connection = pysftp.Connection(*self._sftp_args, **self._sftp_kwargs)
     
            for filename, remote_dir in zip(files, remote_dirs):
                self.put( filename, remote_dir )
                uploaded_files += 1
    
            self.connection.close()

        except:
            print( "Error : upload_files(self, %s, remote_dirs=%s)" % (str(files), str(remote_dirs)) )
        
        return uploaded_files


    def put(self, filename, remote_dir):

        assert os.path.exists(filename),           "Filename '%s' non-existent."  % (filename)
        assert self.connection.exists(remote_dir), "Destination has no dir '%s'" % (remote_dir)

        self.connection.put( filename )
        command =  "mv %s %s." % (os.path.basename(filename), remote_dir)
        self.connection.execute( command )




    def download_files(self):   # files are self._remote_filenames

        self.connection = pysftp.Connection(*self._sftp_args, **self._sftp_kwargs)

        for remote_file, local_file in zip(self._remote_filenames, self._filenames):
            assert self.connection.exists(remote_file)
            self.connection.get( remote_file )
            os.rename( os.path.basename(remote_file), local_file )

        self.connection.close()


    def issue_command(self, command):
        self.connection = pysftp.Connection(*self._sftp_args, **self._sftp_kwargs)
        response = self.connection.execute(' '.join(command))  # command should return a list of files.
        print "Message from remote:"
        for r in response:
            print r
        self.connection.close()
        self.finished = True


    def is_remote_style_present(self):

        # check if present
        self.connection = pysftp.Connection(*self._sftp_args, **self._sftp_kwargs)
        present = self.connection.exists( self.remote_style_path )
        self.connection.close()

        return present


    def construct_command(self):
        command = ['python2', 'wxArt_server.py', self.remote_style_path]
        return command


    def count_remote_files(self):
        connection = pysftp.Connection(*self._sftp_args, **self._sftp_kwargs)
        presents_check = [connection.exists( path ) for path in self._remote_filenames]
        connection.close()
        return np.sum( presents_check )


    def run(self):

        command = self.construct_command()

        self.worker = threading.Thread(name='worker', target=self.issue_command, args=(command,))

        files      = [self.content_path, self.network_path]                 # files to upload to the server
        remote_dirs= [wxArt_server.CONTENTDIR, wxArt_server.NETWORKDIR]     # directories where to load them.

        # add style to these lists, if it is not present yet on the server.
        if not self.is_remote_style_present():
            files.append( self.style_path )
            remote_dirs.append( wxArt_server.STYLEDIR )

        self.upload_files(files, remote_dirs) # Upload the files to newton.

        self.worker.start() # self.issue_command(command)

        dialog = wx.ProgressDialog("Berechnungsfortschritt", "Noch zu verbleibende Zeit", self._pb_max, style=self._pb_style)
        keepGoing = (True, False)
        self.finished = False
        count = 0

        while keepGoing[0] and not self.finished and count < self._pb_max:
            keepGoing = dialog.Update(count)
            wx.Sleep(1) # sleep for 1 second.
            count = self.count_remote_files()

        self.connection.close() # This kills the worker, the connection and the remote process.
        dialog.Destroy()

        # Now we can gather the results.
        self.download_files()


    def query_password(self):

        if not os.path.exists(self._server_path):
            wx.MessageBox("Something went terribly wrong.")
            return
        
        while True: # XXX
            dialog = PasswordQuery(None, size=wx.Size(300, 50), title=self._pwd_title)
            dialog.ShowModal()

            self._sftp_kwargs["password"] = dialog.password
            
            if self.upload_files([self._server_path]) > 0:   # Returns number of successfully uploaded files.
                break                                        # The server file has to be uploaded anyway.

        #self.upload_files([self._server_path])   # XXX
        # initialize the server
        self.connection = pysftp.Connection(*self._sftp_args, **self._sftp_kwargs)
        self.connection.execute("python wxArt_server.py --init")
        self.connection.close()