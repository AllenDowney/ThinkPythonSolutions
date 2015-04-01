"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

This program started with a recipe by Noah Spurrier at
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/521918

"""

import os, sys
from swampy.Gui import *
import Image as PIL      # to avoid name conflict with Tkinter
import ImageTk
import Tkinter

class ImageBrowser(Gui):
    """An image browser that scans the files in a given directory and
    displays any images that can be read by PIL.
    """
    def __init__(self):
        Gui.__init__(self)

        # clicking on the image breaks out of mainloop
        self.button = self.bu(command=self.quit, relief=Tkinter.FLAT)

    def image_loop(self, dirname='.'):
        """loop through the files in (dirname), displaying
        images and skipping files PIL can't read.
        """
        files = os.listdir(dirname)
        for file in files:
            try:
                self.show_image(file)
                print file
                self.mainloop()
            except IOError:
                # probably not an image file
                continue
            except:
                # some other error occurred
                break

    def show_image(self, filename):
        """Use PIL to read the file and ImageTk to convert
        to a PhotoImage, which Tk can display.
        """
        image = PIL.open(filename)
        self.tkpi = ImageTk.PhotoImage(image)
        self.button.config(image=self.tkpi)


def main(script, dirname='.'):
    g = ImageBrowser()
    g.image_loop(dirname)


if __name__ == '__main__':
    main(*sys.argv)
