
import sys
import os
import argparse

if __name__ == "__main__":

    from wxArt.app import App


    description = "wxArt is a deep art interface."

    parser = argparse.ArgumentParser(prog='wxArt', description=description)
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-f', '--fps', default=7, type=int)
    args = parser.parse_args()
    
    app = App(debug=args.debug, fps=args.fps, redirect=False)
    app.MainLoop()
