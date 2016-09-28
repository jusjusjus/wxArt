
import os
import wx


class StyleButton(wx.BitmapButton):

    _root_dir = os.path.dirname(__file__) + "/../resources/models/"
    _defaultImage_path = os.path.dirname(__file__) + "/../resources/default_picture.jpg"

    def __init__(self, *args, **kwargs):

        super(StyleButton, self).__init__(*args, **kwargs)

        self.style_model_path = None
        self.load_image(self._defaultImage_path)


    def get_style_model(self):

        assert os.path.exists(self.path_to_image), "Path to image '{}' not available.".format(self.path_to_image)

        basename = os.path.basename(self.path_to_image).split('.')[0]

        self.style_model_path = self._root_dir + basename + '.model'

        assert os.path.exists(self.style_model_path), "Style model '{}' not available.".format(self.style_model_path)

        return self.style_model_path


    def load_image(self, image_path):
        self.path_to_image = image_path
        bitmap = wx.Image(image_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.SetBitmap(bitmap)


    def get_path_to_image(self):
        return self.path_to_image


    def image_fit(self):
        # get size
        width, height = self.GetSize()

        # load image and get aspect ratio
        image_path = self.get_path_to_image()
        image = wx.Image(image_path,wx.BITMAP_TYPE_ANY)
        Iwidth, Iheight = image.GetSize()
        aspect_ratio = float(Iwidth)/Iheight

        # compute possible sizes
        dummy_height = float(width)/aspect_ratio
        dummy_width = height*aspect_ratio

        # choose size that fits
        if width<dummy_width:
            image = image.Rescale(width,dummy_height,wx.IMAGE_QUALITY_HIGH)
        else:
            image = image.Rescale(dummy_width,height,wx.IMAGE_QUALITY_HIGH)
        bitmap = image.ConvertToBitmap()
        self.SetBitmap(bitmap)
