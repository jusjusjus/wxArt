#!/usr/bin/python

import os
import argparse
import shutil






###########################
# The structure should be #
###########################
# wxArt_files/styles/style1.jpg
# wxArt_files/styles/rembrandt.jpg
# wxArt_files/styles/...
# wxArt_files/content/content.jpg
# wxArt_files/figures/deepart_1.jpg
# wxArt_files/figures/deepart_2.jpg
# wxArt_files/figures/deepart_3.jpg
# wxArt_files/figures/...

MAINDIR = 'wxArt_files/'

STYLEDIR    = MAINDIR + 'styles/'
CONTENTDIR  = MAINDIR + 'content/'
FIGUREDIR   = MAINDIR + 'figures/'

CONTENTNAME = 'content.jpg'
CONTENTPATH = CONTENTDIR + CONTENTNAME

FIGUREBASE  = 'deepart_'
NUM_FIGURES = 6
FIGUREPATHS = ["%s%s%i.jpg" % (FIGUREDIR, FIGUREBASE, i) for i in range(NUM_FIGURES)]


class wxArt_server(object):

    _iterations = 200
    _size       = 256
    _program = 'neural_style.lua' # dummy name

    def __init__(self, style):
        assert os.path.exists(style), "Artistic style '%s' non-existent." % style
        wxArt_server.cleanup_figures() # Remove all old figures from previous computation.
        self.style = style

        shutil.copy(CONTENTPATH, FIGUREPATHS[0])    # FIGUREPATHS[0] is the original file.

        self.content_layers = 'relu4_2'
        self.style_layers   = 'relu1_1,relu2_1,relu3_1,relu4_1,relu5_1'


    def run(self):

        for i in xrange(NUM_FIGURES-1):
            self.execute(FIGUREPATHS[i], FIGUREPATHS[i+1], self.alpha[i])


    def execute(self, input, output, alpha):

        style_weight   = 1e3
        content_weight = 5e0

        command = ['th',              self._program,
                   '-style_image',    self.style,
                   '-content_image',  input,
                   '-style_weight',   style_weight,
                   '-content_weight', content_weight,
                   '-style_layers',   self.style_layers,
                   '-content_layers', self.content_layers,
                   '-output_image',   output,
                   '-num_iterations', self._iterations,
                   '-image_size',     self._size,
                   '-init',           'image']  # Initialize with input image.

        subprocess.call(command)


    @staticmethod
    def make_directory_structure():
        for DIR in [ MAINDIR, STYLEDIR, CONTENTDIR, FIGUREDIR ]:
            if not os.path.exists(DIR):
                os.mkdir( DIR )


    @staticmethod
    def cleanup_figures():
        for figure in FIGUREPATHS:
            os.remove(figure)





if __name__ == "__main__":
    description="wxArt_server is automatically copied to this location by the wxArt-Interface."
    parser = argparse.ArgumentParser(prog='wxArt_server', description=description)

    parser.add_argument( "-i",
                         "--init",
                         help   = "initialize wxArt_server.",
                         action = "store_true")

    parser.add_argument( "style",
                         type    = str,
                         nargs   = "?",
                         help    = "artistic style file to use.")

    args = parser.parse_args()

    # If called with --init, make the directory str...
    if args.init == True:
        wxArt_server.make_directory_structure()
        exit(0)

    # If called with a style, start the server.
    server = wxArt_server(args.style)

    server.run()
