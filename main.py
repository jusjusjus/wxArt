
import sys
import os
import argparse

if __name__ == "__main__":
    description="wxArt is a deep art interface."
    parser = argparse.ArgumentParser(prog='wxArt', description=description)
    #parser.add_argument(
    #    "file",
    #    type    = str,
    #    nargs   = "?",
    #    help    = "edf file to open"
    #)
    #args = parser.parse_args()
    #file = args.file
    #assert file is None or os.path.isfile(args.file), "Could not open file."
    
    from wxArt.app import App
    app = App(redirect=False)
    #if file is not None:
        #app.open_file(args.file)
    app.MainLoop()
