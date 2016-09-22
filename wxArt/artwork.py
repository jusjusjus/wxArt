

from .image import Image
from .fns.generate import ChainerFNS


class Artwork(Image):

    _output_path = './artwork.jpg'

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



    def load_video(self, video_path): # video_path zeigt auf nen gif
        pass
