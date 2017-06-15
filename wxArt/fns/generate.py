
from __future__ import print_function
import os
import numpy as np
from PIL import Image as PILImage
import time

import chainer
import logging
from chainer import cuda, Variable, serializers
from net import FastStyleNet




class ChainerFNS(FastStyleNet):

    logger = logging.getLogger(name='ChainerFNS')

    def __init__(self, gpu=-1):

        super(ChainerFNS, self).__init__()

        self.style_path = None

        if gpu >= 0:
            cuda.get_device(gpu).use()
            self.to_gpu()


    def set_style(self, style):

        assert os.path.exists(style), "Style file '{}' not available.".format(style)

        if not self.style_path == style:
            serializers.load_npz(style, self)


    
    def generate(self, inputpath, outputpath=None):
        start = time.time()
        image = np.asarray(PILImage.open(inputpath).convert('RGB'), dtype=np.float32).transpose(2, 0, 1)
        image = image.reshape((1,) + image.shape)
        x = Variable(image)

        # Performs the call defined in the FastStyleNet
        # class in ./net.py on the input reshaped image
        y = self(x)
        result = cuda.to_cpu(y.data)
        
        result = result.transpose(0, 2, 3, 1)
        result = result.reshape((result.shape[1:]))
        result = np.uint8(result)
        self.logger.info("Elapsed time: %.3g" % (time.time() - start))

        if not outputpath == None:
            PILImage.fromarray(result).save(outputpath)

        return result
    





if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Real-time style transfer image generator')
    parser.add_argument('input') # image to repaint
    parser.add_argument('--gpu', '-g', default=-1, type=int,
                        help='GPU ID (negative value indicates CPU)')
    parser.add_argument('--model', '-m', default='models/style.model', type=str)
    parser.add_argument('--out', '-o', default='out.jpg', type=str)
    args = parser.parse_args()

    # Define an instance of the class holding all the chainer code
    model = ChainerFNS(gpu=args.gpu)
    # Assign a style model
    model.set_style(args.model)

    # Perform the style transfer on the input image
    image = model.generate(args.input)

    image.save(args.out)
