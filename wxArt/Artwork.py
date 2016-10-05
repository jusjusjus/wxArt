
import wx
import tempfile
from .AnimatedDisplay import AnimatedDisplay
from .fns.generate import ChainerFNS
import subprocess
import numpy as np
import os


class Artwork(AnimatedDisplay):

    _output_path = './artwork.jpg'
    _pb_style = wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME

    default_kwargs = dict(temp_dir = '.')

    def __init__(self, *args, **kwargs):

        for att in self.default_kwargs.keys():
            if kwargs.has_key(att):
                setattr(self, att, kwargs.pop(att))
            else:
                setattr(self, att, self.default_kwargs[att])

        self.processor = ChainerFNS(gpu=-1)
        super(Artwork, self).__init__(*args, **kwargs)
        self.frames = None  # Frames are handles inconsistently among member functions.
        # mkdir for archiving files if it doesn't yet exist.


    def set_style(self, style):
        self.style_path = style
        self.processor.set_style(style)


    def process_frames(self, frames):

        num_frames = len(frames)

        progress = wx.ProgressDialog("Berechnungsfortschritt",
                                     "Noch zu verbleibende Zeit",
                                     num_frames,
                                     style=self._pb_style)

        keepGoing = progress.Update(0)  # Initialize

        processed_frames = []
        for idx_f in xrange(num_frames):
            self.processor.generate(frames[idx_f][0],
                                    frames[idx_f][0])
            processed_frames.append( frames[idx_f] )
            keepGoing = progress.Update(idx_f)

            if not keepGoing[0]:
                break

        progress.Show(False)

        # delete the frames that have not been processed
        for i_del in xrange(idx_f + 1, num_frames):
            try:
                subprocess.call(['rm', frames[i_del][0]])
            except WindowsError:
                if os.path.exists(frames[i_del][0]):
                    os.remove(frames[i_del][0])

        return processed_frames
        

    def convert_to_artwork(self, fps=None):
        suffix = os.path.basename(self.path_to_image).split('.')[1]

        if suffix == 'gif': # it's a gif video
            self.convert_gif_to_artwork(fps)

        else:   # it's a jpg
            self.convert_jpg_to_artwork()


    def convert_gif_to_artwork(self, fps):
        assert not fps == None, "Fps cannot be none."

        self.Stop()
        frames = self.get_frames_to_process()               # Check for available files in the folder
        processed_frames = self.process_frames(frames)      # Convert all frames to artworks.

        for fi, fo in processed_frames:
            self.fit_and_save(fi, fo) # fi contains the artwork now!!!

        self.merge_to_gif(fps=fps)  # Merge all processed and enlarged frames into one movie.
        self.LoadFile(self._gif_path)
        self.Play()


    def convert_jpg_to_artwork(self):   # load_image sets input_image

        output_path = tempfile.mkstemp(prefix = 'artwork_',
                                       suffix = '.jpg',
                                       dir    = self.temp_dir)[1]

        self.processor.generate(self.path_to_image, output_path)
        super(Artwork, self).load_image(output_path)  # this only sets path_to_image


