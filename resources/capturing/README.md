# Camera capturing troubleshooting

## Wrong camera feed

If you have more than camera available, be sure to address the correct one.

The *bash* command `ls /dev | grep video` provides a list of all available cams.

Now all you have to do to use another video feed is to provide the last digit of the video device with the flag `-v` in the command line.

```{bash}
# Use an external USB cam assigned to /dev/video1
python main.py -v 1
```

## No camera feed at all

You are just seeing the default picture and no video is captured at all? Here is some little troubleshooting guide to check your cam settings. 

This guide is written for an Ubuntu16.04 machine but should work on all (Debian-)Linux distributions.

### Check the Python API of OpenCV (Open computer vision)

First of all let's check if there is really a problem with the cam.

Under the hood the wxArt project uses the **cv2** module of Python 2 (installed via `pip install opencv-python`).

Let's open an ipython2 shell and try to capture an image using the (default) cam. (If you have a different device, try a higher integer - the number obtained in the next section).

```{python}
import cv2

cam = cv2.VideoCapture( 0 )
s, img = cam.read()

s, img
```

*s* is *False* and *img* is *None*? Then there is really a problem with the cam.

### Check device

Okay, now that we really now that there is an issue with the cam, let's check if it is working at all. For this you can e.g. use the *VLC* player as following.

```{bash}
# Check how your camera is called
ls /dev | grep video
# Note the number[s] after video and use it in the following command
vlc v4l2:///dev/video0
```

If you see the video feed of your web cam, then it's a Python issue.

### Check your OpenCV (Open computer vision) installation

Since Python is not able to capture video but the cam is working, we will check whether the underlying C++ library is working properly.

Therefore I wrote a little [C++ script](/resources/capturing/camera-test.cpp) capturing an image every 30 second and displaying just the edges detected in it.

In line 6 of the script the variable *cap* is defined. Its input has to be the device number obtained in the previous section!

Before going on, be sure you installed both `cmake` and `libopencv-dev`.

Now we will use *cmake* to compile the script to test the camera and call it.

```{bash}
cmake .
make
./camera-test
```

Is it working? Well, then it is an issue of the Python wrapper *opencv-python* (as it was in my case).

### Compile newest OpenCV from source

Since we have a working OpenCV installation and a Python module which refuses to talk with it, there is most probably a lag in time/some major changes between both versions.

To sync those two, first uninstall the *opencv-python* version delivered via pip.

```{bash}
sudo pip uninstall opencv-python
```

Now get the latest [OpenCV](https://github.com/opencv/opencv) version (3.2.0 for me right now) and [compile](http://docs.opencv.org/master/d7/d9f/tutorial_linux_install.html) it.

```{bash}
# Clone the OpenCV package
git clone https://github.com/opencv/opencv

# Compile the package. See instructions in link above.
cd opencv
mkdir build
cd build

cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local ..

make -j7 # runs 7 jobs in parallel
sudo make install

# P.S.: I'm not really a C++ or cmake guru. So got an 
# "error adding symbols: DSO missing from command line" error. 
# You can circumvent this by commenting first line in the 
# CMakeLists.txt file and hit 'make' and all following
# commands in the parent folder. ;)
```

Afterwards you have a brand new version of *opencv-python* installed.

Test it using one of the OpenCV [example scripts](https://github.com/opencv/opencv/blob/master/samples/python/video.py).

```{bash}
# At the root of the OpenCV repository tree
cd samples/python

# Run the sample script with the identifier of your cam
# (see above) as the first argument
python video.py 0
```

Now your should see your cam feed.

