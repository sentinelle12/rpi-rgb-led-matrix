# =============================image-viewer.py=============================
import time
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

if len(sys.argv) < 2:
    sys.exit("Require an image argument")
else:
    image_file = sys.argv[1]

image = Image.open(image_file)

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)


# ====================INSERT IMAGE CONCATENATOR======================

# Make image fit our screen.
image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

matrix.SetImage(image.convert('RGB'))

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)

# ===============================================================================

from PIL import Image, ImageDraw, ImageFont
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics


def get_concat_h(im1, im2, im3):
    dst = Image.new('RGB', (im1.width + im2.width + im3.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    dst.paste(im3, (im1.width + im2.width, 0))
    return dst


canvas = RGBMatrix.matrix.CreateFrameCanvas()

fnt = ImageFont.truetype('./nhl_matrix/nhl_fonts/arial.ttf', 40)

while True:
    im1 = Image.new('RGB', (64, 32), (255, 255, 255))
    im2 = Image.new('RGB', (128, 32), (255, 255, 255))
    im3 = Image.new('RGB', (64, 32), (255, 255, 255))

    draw1 = ImageDraw.Draw(im1)
    draw1.text((30, 30), u'Hello World', font=fnt, fill=(0, 0, 255, 128))
    draw2 = ImageDraw.Draw(im2)
    draw2.text((30, 30), u'Hello World', font=fnt, fill=(0, 0, 255, 128))
    draw3 = ImageDraw.Draw(im2)
    draw3.text((30, 30), u'Hello World', font=fnt, fill=(0, 0, 255, 128))

    im_pil = get_concat_h(im1, im2, im3)
    canvas.SetImage(im_pil)
    canvas = RGBMatrix.matrix.SwapOnVSync(canvas)
