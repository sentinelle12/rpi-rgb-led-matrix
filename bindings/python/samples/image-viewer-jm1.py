#!/usr/bin/env python
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

#if len(sys.argv) < 2:
#    sys.exit("Require an image argument")
#    image_file = "../nhl_matrix/nhl_logos/logo_8.gif"
#else:
#    image_file = sys.argv[1]

#image = Image.open(image_file)

home_img_path = "../nhl_matrix/nhl_logos/sources/logo_8.gif"
away_img_path = "../nhl_matrix/nhl_logos/logo_2.gif"

home_logo = Image.open(home_img_path)
away_logo = Image.open(away_img_path)

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

# Make image fit our screen.
#image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
home_logo.thumbnail((matrix.width/2.2, matrix.height/2.2), Image.ANTIALIAS)
away_logo.thumbnail((matrix.width/2.2, matrix.height/2.2), Image.ANTIALIAS)

matrix.SetImage(home_logo.convert('RGB'), 1, 1)
matrix.SetImage(away_logo.convert('RGB'), 1 + home_logo.width + 4, 1)



try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)
