# wxArt
wxArt is a wxpython interface to control a deep-art server.

We humbly wrap the wonderful code from yusuketomoto (MIT licensed):

https://github.com/yusuketomoto/chainer-fast-neuralstyle

and use the great models given by gafr:

https://github.com/gafr/chainer-fast-neuralstyle-models

# Installation

To run this application you have to install the following Python packages

```{bash}
pip install chainer wxPython opencv-python scikit-image
```

If the installation of *wxPython* fails, try to install it manually via the package repositories.

```{bash}
# In Ubuntu16
sudo apt update
sudo apt install wxPython
```

# Running the application

To run the application, just type the following command in your terminal

```{bash}
python main.py
```

# Troubleshooting

You are not able to capture any images with your webcam? See this little [guide](/resources/capturing/README.md) to resolve your problem.


# Further dependencies

* openCV
* [PDFtk](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/)
* Latex, e.g [MikTex](http://miktex.org/) under Windows

