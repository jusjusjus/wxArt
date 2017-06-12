
import sys
import os
import logging
import argparse

if __name__ == "__main__":

    from wxArt.wxArt import wxArt


    description = "wxArt is a deep art interface."

    parser = argparse.ArgumentParser(prog='wxArt', description=description)
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('--email', action='store_true')
    parser.add_argument('-f', '--fps', default=7, type=int)
    # Number of the video device to connect to. The default is \dev\video0
    parser.add_argument('-v', '--video', default=0, type=int )
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    app = wxArt(debug=args.debug, fps=args.fps, email=args.email, redirect=False,
                  video=args.video)
    app.MainLoop()
