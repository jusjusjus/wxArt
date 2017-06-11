

import wx
import os
import sys
from .Artwork import Artwork
import subprocess



class Postcard(object):

    _artwork_file   = Artwork._output_path

    _pdf_dir        = os.path.dirname(sys.argv[0]) + "/"
    _tex_dir        = os.path.dirname(__file__) + "/../resources/postcards/"
    _tex_name       = "default.tex"
    _mrg_name       = "merger.tex"

    def __init__(self, parent):
        self.parent       = parent
        self.artwork_file = Artwork._output_path

        self.pdf_dir = self._pdf_dir
        self.tex_dir = self._tex_dir
        self.tex_name= self._tex_name
        self.mrg_name= self._mrg_name

        self.init_names()


    def init_names(self):
        self.tex_file = self.tex_dir + self.tex_name
        self.mrg_file = self.tex_dir + self.mrg_name
        self.pdf_name = self.tex_name.split('.')[0] + '.pdf'
        self.pdf_file = self.pdf_dir + self.pdf_name


    def create(self):

        assert os.path.exists(self.artwork_file), "Artwork not present."
        assert os.path.basename(self.artwork_file).split('.')[1] == 'jpg', "Artwork required to be a jpeg."

        self.compile_tex()
        self.create_postcard()
        self.show_postcard()


    def compile_tex(self):
        # The OpenCV package seems to not set the resolution within
        # the header of the JPEGs right. Therefore PDFLaTeX doesn't
        # know the DPI and the corresponding unit and considers the
        # e.g. 300px x 300px as 300in x 300in, which would be way
        # to big. Therefore it does include the image in the pdf
        # (you can still extract it using pdfimages -j default.pdf
        # extracts-) but does not display it.
        # Therefore we have to add the correct DPI to the header
        # ourselves.
        os.system( "exiftool artwork.jpg -jfif:Xresolution=300 -jfif:Yresolution=300 -jfif:ResolutionUnit=inch" )
        # Copy the artwork file into the postcard folder
        os.system( "cp ./artwork.jpg " + self.tex_dir + "artwork.jpg" )
        subprocess.call(['pdflatex', self.tex_file])


    def create_postcard(self):
        # Split the .tex-output into separate pages.
        subprocess.call(['pdftk', self.pdf_file, 'burst'])
        # Join the second page 4 times as front of the postcard.
        subprocess.call(['pdftk', 'pg_0001.pdf', 'pg_0001.pdf', 'pg_0001.pdf', 'pg_0001.pdf', 'cat', 'output', 'page_1.pdf'])
        # Join the third page 4 times as back of the postcard.
        subprocess.call(['pdftk', 'pg_0002.pdf', 'pg_0002.pdf', 'pg_0002.pdf', 'pg_0002.pdf', 'cat', 'output', 'page_2.pdf'])
        # Join the two results.
        subprocess.call(['pdftk', 'page_1.pdf', 'page_2.pdf', 'cat', 'output', 'to_print_4x4.pdf'])

        subprocess.call(['pdflatex', self.mrg_file])
        # Cleanup temporary files.
        os.system( 'rm ' + './pg_* ' + './page_* ' + './default*' )


    def show_postcard(self, filename='merger.pdf'):
        try:
            subprocess.call(['evince', filename])
        except WindowsError:
            # open with default program
            os.system('start ' + filename)


