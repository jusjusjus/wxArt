

from .image import Image
from .fns.generate import ChainerFNS
import subprocess
import os


class Artwork(Image):

    _output_path = './artwork.jpg'
    _gif_path = './artwork.gif'

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


    def load_images(self, fps):

        for i in xrange(1000):
            frame = 'frame_%03i.jpg' % (i)
            conv_frame = 'conv_frame_%03i.jpg' % (i)

            if os.path.exists(frame):
                print 'Processing ..', frame
                self.processor.generate(frame, conv_frame)

            else:
                break

        subprocess.call(['rm', self._gif_path])
        subprocess.call(['ffmpeg', '-f', 'image2', '-framerate', str(fps), '-i', 'conv_frame_%03d.jpg', self._gif_path])
        self.LoadFile(self._gif_path)
        self.Play()

