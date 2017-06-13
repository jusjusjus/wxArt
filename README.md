![screenshot](resources/screenshot.jpg)

# Features

- Take a snapshot or a short video and redraw it in the style of a famous painting
- Choose your style among 11 iconic artworks
- Create postcards with your redrawn pictures


# wxArt

wxArt implements the neural art method presented in the [A Neural Algorithm of Artistic Style](https://arxiv.org/pdf/1508.06576.pdf) paper by Leon A. Gatys, Alexander S. Ecker, and Matthias Bethge.

It decomposes an image into two different representations, its style and content, and is also able to recombine those two to a new picture quite similar to the original one. But one does not have to join the two representations of one and the same image. It's also possible to recombine the style of one picture with the content of another. And this is where the fun begins.

We took 11 iconic paintings and extracted their style information. With the help of the wxArt app the user can take/load a picture using e.g. her webcam and the app will get its content and recombine it with the style of her choice.

wxArt is a wxpython interface to control a deep-art server.

We humbly wrap the wonderful code from yusuketomoto (MIT licensed):

https://github.com/yusuketomoto/chainer-fast-neuralstyle

and use the great models given by gafr:

https://github.com/gafr/chainer-fast-neuralstyle-models

# Installation

## Ubuntu

To run this application you have to install the following Python packages via your operation system's repository (recommended)

```{bash}
sudo apt update
sudo apt install wxPython python-opencv python-skimage
sudo pip install chainer
```

or *pip*

```{bash}
sudo pip install chainer wxPython opencv-python scikit-image
```

In order to compile [postcards](resources/postcard_example.pdf) containing the transformed image with LaTeX, be sure to have the following packages installed.

```{bash}
sudo apt install texlive-lang-german pdftk libimage-exiftool-perl
```

## Suse

In Suse install the following packages from your repositories

```{bash}
sudo zypper refresh
sudo zypper python-wxWidgets-3_0 python-opencv python-pip
```

Afterwards install the remaining packages using *pip*

```{bash}
sudo pip2 install scikit-image chainer
```

# Running the application

To run the application, just type the following command in your terminal

```{bash}
python main.py
```

If you want to be able to send the transformed pictures by mail, start the script using the `--email`` flag.

```{bash}
python main.py --email
```

# Train your own models

The *wxArt* package is not restricted to the 11 styles trained by the authors. You are free to train your own one! But there are a number of requirements you have to fulfill. 

- A powerful Nvidia GPU capable of running [Cuda](https://www.nvidia.com/object/cuda_home_new.html). Of course, in principle you could also train on a CPU but this would last forever. If you don't own one yourself, check out the e.g. the [Amazon compute cloud](https://aws.amazon.com/ec2/).
- A large training set of photographs
- The [VGG-16 model](http://www.robots.ox.ac.uk/%7Evgg/research/very_deep/) to start the optimization from
- A picture you want to learn the style from

## Obtain a training set

We will use the [MSCOCO](http://mscoco.org/dataset/#overview) image set as our default training set. There is also an [API](https://github.com/pdollar/coco) available for automating the download but unfortunately its PythonAPI is, of course, not working and in the LuaAPI a function for downloading the entire data set is not implemented. So you have to download it [directly](http://msvocds.blob.core.windows.net/coco2014/train2014.zip).

## Obtain the VGG-16 model

To download and convert the VGG-16 model, just call the [following](wxArt/fns/setup_model.sh) bash function

```{bash}
# In /wxArt/fns
./setup_model.sh
```

## Train a new model

Now you can train a new model using the following line of code

```{bash}
# In /wxArt/fns
python train.py -g 0 -d <PATH_TO_MSCOCO_SET> -s <PATH_TO_YOUR_STYLE_IMAGE> -o new_model
```


# Troubleshooting

You are not able to capture any images with your webcam? See this little [guide](/resources/capturing/README.md) to resolve your problem.


# Further dependencies

* openCV
* [PDFtk](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/)
* Latex, e.g [MikTex](http://miktex.org/) under Windows

