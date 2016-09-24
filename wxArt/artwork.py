
import wx
from .image import Image
from .fns.generate import ChainerFNS
import subprocess
import os


class Artwork(Image):

    _output_path = './artwork.jpg'
    _gif_path = './artwork.gif'
    _pb_style = wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME

    def __init__(self, *args, **kwargs):
        self.processor = ChainerFNS(gpu=-1)
        super(Artwork, self).__init__(*args, **kwargs)


    def set_style(self, style):
        self.style_path = style
        self.processor.set_style(style)


    def load_image(self, image_path):
        self.path_to_image = image_path
        self.processor.generate(self.path_to_image, self._output_path)
        super(Artwork, self).load_image(self._output_path)


    def get_frames_to_process(self):

        frames = []
        for i in xrange(1000):
            frame = 'frame_%03i.jpg' % (i)

            if os.path.exists(frame):
                frames.append(frame)

        return frames


    def process_frames(self, frames):

        num_frames = len(frames)

        dialog = wx.ProgressDialog("Berechnungsfortschritt", "Noch zu verbleibende Zeit", num_frames, style=self._pb_style)
        keepGoing = dialog.Update(0)    # Initialize


        for idx_f in xrange(num_frames):
            self.processor.generate(frames[idx_f], frames[idx_f])
            keepGoing = dialog.Update(idx_f)

            if not keepGoing[0]:
                break

        dialog.Show(False)

        # delete the frames that have not been processed
        for i_del in xrange(idx_f+1, num_frames):
            subprocess.call(['rm', frames[i_del]])


    def merge_to_gif(self, fps):
        subprocess.call(['rm', self._gif_path])
        subprocess.call(['ffmpeg', '-f', 'image2', '-framerate', str(fps), '-i', 'frame_%03d.jpg', self._gif_path])


    def load_images(self, fps):

        frames = self.get_frames_to_process()   # Check for available files in the folder

        self.process_frames(frames)             # Convert all frames to artworks.

        self.merge_to_gif(fps = fps)            # Merge all artworks into one movie.

        self.LoadFile(self._gif_path)
        self.Play()


