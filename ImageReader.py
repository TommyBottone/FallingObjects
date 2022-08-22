from PIL import Image
import numpy as np
import os
from PIL.ExifTags import TAGS, GPSTAGS
import threading


class XY:
    _x = 0
    _y = 0

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __init__(self):
        return

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def setX(self, x):
        self._x = x

    def setY(self, y):
        self._y = y


class ImageMetaData:
    #the color locations in the array
    _r = 0
    _g = 1
    _b = 2
    #stored color to ignore
    _ignoreR = 0
    _ignoreG = 0
    _ignoreB = 0

    _topLeft = XY()
    _bottomRight = XY()

    def __init__(self):
        return

    def _findBottomRight(self):
        width = self._image.size[0]
        height = self._image.size[1]
        for x in reversed(range(width)):
            for y in reversed(range(height)):
                valr, valg, valb = self._rgb_image.getpixel((x, y))
                if valr == self._ignoreR and valg == self._ignoreG and valb == self._ignoreB:
                    continue
                else:
                    print(x, y, valr, valg, valb, self._ignoreR, self._ignoreG,
                          self._ignoreB)
                    self._bottomRight.setX(x)
                    self._bottomRight.setY(y)
                    return

    def _findTopLeft(self):
        width = self._image.size[0]
        height = self._image.size[1]
        for x in range(width):
            if x == 0:
                continue
            for y in range(height):
                if y == 0:
                    continue
                else:
                    valr, valg, valb = self._rgb_image.getpixel((x, y))
                    if valr == self._ignoreR and valg == self._ignoreG and valb == self._ignoreB:
                        continue
                    else:
                        print(x, y, valr, valg, valb, self._ignoreR,
                              self._ignoreG, self._ignoreB)
                        self._topLeft.setX(x)
                        self._topLeft.setY(y)
                        return

    def findRectangle(self, imagename):
        #assume 0,0 is fine
        self._ignoreR, self._ignoreG, self._ignoreB = self._rgb_image.getpixel(
            (0, 0))

        self._findTopLeft()
        print(self._topLeft.getX(), self._topLeft.getY())
        self._findBottomRight()
        print(self._bottomRight.getX(), self._bottomRight.getY())
        return

    def readImage(self, imagename):
        self._image = Image.open(imagename)
        self._rgb_image = self._image.convert('RGB')
        info_dict = {
            "Filename": self._image.filename,
            "Image Size": self._image.size,
            "Image Height": self._image.height,
            "Image Width": self._image.width,
            "Image Format": self._image.format,
            "Image Mode": self._image.mode,
            "Image is Animated": getattr(self._image, "is_animated", False),
            "Frames in Image": getattr(self._image, "n_frames", 1)
        }
        for label, value in info_dict.items():
            print(f"{label:30}: {value}")

        exifdata = self._image.getexif()
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)

            if isinstance(data, bytes):
                data = data.decode()
            print(f"{tag:30}: {data}")

        self.findRectangle(imagename)
        imgcrop = self._image.crop((self._topLeft.getX(),self._topLeft.getY(), self._bottomRight.getX(),self._bottomRight.getY()))
        cropname = os.path.splitext(imagename)[0]
        cropname = cropname + "copy.jpg"
        imgcrop.save(cropname)
