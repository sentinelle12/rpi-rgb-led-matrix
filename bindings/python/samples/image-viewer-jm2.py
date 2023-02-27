#!/usr/bin/env python
import time
import sys

from samplebase import SampleBase
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

class Logo(Image):
    def __init__(self, image_file, thmbn_width, thmbn_height):
        super(Logo, self).__init__()
        self.image = Image.open(image_file)
        self.image.thumbnail((thmbn_width, thmbn_height), Image.ANTIALIAS)

class Matrix(SampleBase):
    def __init__(self):
        super(Matrix, self).__init__()
        self.options.rows = 64
        self.options.cols = 64
        self.options.chain_length = 1
        self.options.parallel = 1
        self.options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
        # self.matrix = RGBMatrix(options = options)

    def display_image(self, x_pos, y_pos):
        matrix.SetImage(image.convert('RGB'))
        # matrix.SetImage(self.image, x_pos)


try:
    print("Press CTRL-C to stop.")
    while True:
        matrix = Matrix()
        home_logo = Logo('../nhl_matrix/nhl_logos/logo_8.gif')
        away_logo = Logo('../nhl_matrix/nhl_logos/logo_2.gif')

        matrix.display_image(10, 5)
        matrix.display_image(10, 32)

except KeyboardInterrupt:
    sys.exit(0)
