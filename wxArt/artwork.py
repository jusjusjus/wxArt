
import wx
from .image import Image
from .fns.generate import ChainerFNS
import subprocess
import numpy as np
import os


class Artwork(Image):
    _output_path = './artwork.jpg'
    _arxiv_dir = './arxiv/'
    _gif_path = './artwork.gif'
    _pb_style = wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME

    def __init__(self, *args, **kwargs):
        self.processor = ChainerFNS(gpu=-1)
        super(Artwork, self).__init__(*args, **kwargs)
        self.frames = None  # Frames are handles inconsistently among member functions.
        # mkdir for archiving files if it doesn't yet exist.
        if not os.path.exists(self._arxiv_dir):
            os.mkdir(self._arxiv_dir)

    def set_style(self, style):
        self.style_path = style
        self.processor.set_style(style)

    def load_image(self, image_path):
        self.path_to_image = image_path
        self.processor.generate(self.path_to_image, self._output_path)
        super(Artwork, self).load_image(self._output_path)

    # Methods for gif-creation
    def get_frames_to_process(self):
        possible_frames = ('frame_%03i.jpg' % (i) for i in xrange(1000))
        frames = [f for f in possible_frames if os.path.exists(f)]
        return frames

    def process_frames(self, frames):

        num_frames = len(frames)

        progress = wx.ProgressDialog("Berechnungsfortschritt", "Noch zu verbleibende Zeit", num_frames,
                                     style=self._pb_style)
        keepGoing = progress.Update(0)  # Initialize

        for idx_f in xrange(num_frames):
            self.processor.generate(frames[idx_f], frames[idx_f])
            keepGoing = progress.Update(idx_f)

            if not keepGoing[0]:
                break

        progress.Show(False)

        # delete the frames that have not been processed
        for i_del in xrange(idx_f + 1, num_frames):
            subprocess.call(['rm', frames[i_del]])


    def merge_to_gif(self, fps):
        subprocess.call(['rm', self._gif_path])
        subprocess.call(['ffmpeg', '-f', 'image2', '-framerate', str(fps), '-i', 'frame_%03d.jpg', self._gif_path])


    def create_and_load_gif(self, fps):
        frames = self.get_frames_to_process()   # Check for available files in the folder
        self.process_frames(frames)             # Convert all frames to artworks.
        self.merge_to_gif(fps = fps)            # Merge all artworks into one movie.
        self.LoadFile(self._gif_path)
        self.Play()


    def take_video(self, fps):
        self.merge_to_gif(fps=fps)  # Merge all artworks into one movie.
        self.LoadFile(self._gif_path)
        self.Play()


    def create_artwork_gif(self, fps):
        # TODO: add pause here then issue generation of artwork
        self.process_frames(self.frames)  # Convert all frames to artworks.
        self.merge_to_gif(fps=fps)  # Merge all artworks into one movie.
        self.LoadFile(self._gif_path)
        self.Play()


    # Methods for archiving
    def new_arxiv_path(self):
        style = os.path.basename(self.style_path).split('.')[0]  # raw name of the style
        path = self._arxiv_dir + style + '_' + str(np.random.randint(10 ** 7)) + '.jpg'  # ./arxiv/<style>_<randint>.jpg

        return path

    def arxiv(self):
        arxiv_path = self._arxiv_dir  # This one definitely exists.
        while os.path.exists(arxiv_path):  # Was it by chance a name that already exists.
            arxiv_path = self.new_arxiv_path()  # Get a random name.

        subprocess.call(['cp', self.path_to_image, arxiv_path])
