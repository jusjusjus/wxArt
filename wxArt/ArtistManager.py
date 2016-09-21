
import wx
import pysftp
import os
import threading
from .PasswordQuery import PasswordQuery
import wxArt_server
import numpy as np


class ArtistManager(object):

    _sftp_kwargs   = dict(host='newton', username='jschwab', password='') # XXX
    _server_path   = wxArt_server.__file__.strip('c')   # because of the .pyc files

    _remote_filenames = wxArt_server.FIGUREPATHS
    _figuredir = './'
    _filenames = [ _figuredir + os.path.basename(filename)  for filename in _remote_filenames ]

    _pb_max = len(_remote_filenames)
    _pb_style = wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME


    def __init__(self, parent):
        self.parent = parent
        self.sftp_kwargs = self._sftp_kwargs
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
            connection = pysftp.Connection(**self.sftp_kwargs)
     
            for filename, remote_dir in zip(files, remote_dirs):
                self.put( connection, filename, remote_dir )
                uploaded_files += 1
    
            connection.close()

        except:
            print( "Error : upload_files(self, %s, remote_dirs=%s)" % (str(files), str(remote_dirs)) )
        
        return uploaded_files


    def put(self, connection, filename, remote_dir):

        assert os.path.exists(filename),      "Filename '%s' non-existent." % (filename)
        assert connection.exists(remote_dir), "Destination has no dir '%s'" % (remote_dir)

        connection.put( filename )
        command =  "mv %s %s." % (os.path.basename(filename), remote_dir)
        connection.execute( command )


    def download_files(self):   # files are self._remote_filenames

        # Before starting the download, try to delete the old filenames.
        for filename in self._filenames:
            try:    os.remove(filename)
            except: continue

        # Download ..
        connection = pysftp.Connection(**self.sftp_kwargs)
        connection.get_d( wxArt_server.FIGUREDIR, '.' )
        connection.close()

        # .. and rename.
        for remote_file, local_file in zip(self._remote_filenames, self._filenames):
            os.rename( os.path.basename(remote_file), local_file )


    def issue_command(self, command):
        connection = pysftp.Connection(**self.sftp_kwargs)
        response = connection.execute(' '.join(command))  # command should return a list of files.
        print "####################"
        print "Message from remote:"
        print "####################"
        for r in response:
            print r
        connection.close()
        self.finished = True


    def is_remote_style_present(self): # check if the style-file is present remotely.
        connection = pysftp.Connection(**self.sftp_kwargs)
        present = connection.exists( self.remote_style_path )
        connection.close()
        return present


    def construct_command(self):
        command = ['python2', 'wxArt_server.py', self.remote_style_path]
        return command


    def count_remote_files(self):
        connection = pysftp.Connection(**self.sftp_kwargs)
        are_present = [connection.exists( filename ) for filename in self._remote_filenames]
        connection.close()
        return np.sum( are_present )


    def run(self):
        # Construct the server-thread
        command = self.construct_command()
        self.worker = threading.Thread(name='worker', target=self.issue_command, args=(command,))

        # Gather files to copy
        files       = [self.content_path, self.network_path]                 # files to upload to the server
        remote_dirs = [wxArt_server.CONTENTDIR, wxArt_server.NETWORKDIR]     # directories where to load them.

        if not self.is_remote_style_present():  # add style to these lists, if it is not present yet on the server.
            files.append( self.style_path )
            remote_dirs.append( wxArt_server.STYLEDIR )

        # Upload the files
        self.upload_files(files, remote_dirs) # Upload the files to newton.

        # Start the worker
        self.worker.start() # self.issue_command(command).  Makes it's own ssh connection.

        # Start progress bar.   The progress is measured by files that are remotely present.
        dialog = wx.ProgressDialog("Berechnungsfortschritt", "Noch zu verbleibende Zeit", self._pb_max, style=self._pb_style)
        keepGoing = (True, False)
        self.finished = False
        count = 0

        while keepGoing[0] and not self.finished and count < self._pb_max:
            keepGoing = dialog.Update(count)
            wx.Sleep(1) # sleep for 1 second.
            count = self.count_remote_files()   # returns the number of counted files.

        dialog.Destroy()

        # Now we can gather the results.
        self.download_files()    # We found count files; we want to download these.
        

    def query_password(self):

        if not os.path.exists(self._server_path):
            wx.MessageBox("Something went terribly wrong.")
            return
        
        while False: # XXX
            query_fields = [('host',   self.sftp_kwargs['host']),
                            ('username', self.sftp_kwargs['username']),
                            ('password', self.sftp_kwargs['password'])]

            pwd_title = "Compute with.."

            dialog = PasswordQuery(query_fields, None, size=wx.Size(200, 100), title=pwd_title)
            dialog.ShowModal()

            self.sftp_kwargs.update(dialog.input)

            if self.upload_files([self._server_path]) > 0:   # Returns number of successfully uploaded files.
                break                                        # The server file has to be uploaded anyway.

        #self.upload_files([self._server_path])                                 # XXX
        # initialize the server
        #connection = pysftp.Connection(*self._sftp_args, **self._sftp_kwargs)  # XXX
        #connection.execute("python wxArt_server.py --init")                    # XXX
        #connection.close()                                                     # XXX
