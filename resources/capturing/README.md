# Camera capturing troubleshooting

You are just seeing the default picture and no video is captured at all? Here is some little troubleshooting guide to check your cam settings. 

This guide is written for an Ubuntu16.04 machine but should work on all (Debian-)Linux distributions.

## Check the Python API of OpenCV (Open computer vision)

First of all let's check if there is really a problem with the cam.

Under the hood the wxArt project uses the **cv2** module of Python (installed via `pip install opencv-python`).

Let's open an ipython2 shell and try to capture an image using the (default) cam. (If you have a different device, try a higher integer - the number obtained in the next section).

```{python}
import cv2

cam = cv2.VideoCapture( 0 )
s, img = cam.read()

s, img
```

*s* is *False* and *img* is *None*? Then there is really a problem with the cam.

## Check device

Okay, now that we really now that there is an issue with the cam, let's check if it is working at all. For this you can e.g. use the *VLC* player as following.

```{bash}
# Check how your camera is called
ls /dev | grep video
# Note the number[s] after video and use it in the following command
vlc v4l2:///dev/video0
```

If you see the video feed of your web cam, then it's a Python issue.

## Check your OpenCV (Open computer vision) configuration

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

Is it working? Well, then it is an issue of the Python wrapper (package).

