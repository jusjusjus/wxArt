
import os
from .imagebutton import ImageButton


class StyleButton(ImageButton):

    _root_dir = os.path.dirname(__file__) + "/../resources/models/"

    def __init__(self, *args, **kwargs):

        super(StyleButton, self).__init__(*args, **kwargs)

        self.style_model_path = None


    def get_style_model(self):

        assert os.path.exists(self.path_to_image), "Path to image '{}' not available.".format(self.path_to_image)

        basename = os.path.basename(self.path_to_image).split('.')[0]

        self.style_model_path = self._root_dir + basename + '.model'

        assert os.path.exists(self.style_model_path), "Style model '{}' not available.".format(self.style_model_path)

        return self.style_model_path



