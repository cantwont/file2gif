from PIL import Image
from functions.settings import DEBUG_MODE

four_k = (3840, 2160)


def pixels_2_png(pixels, fname, reso=four_k):
    img = Image.new('RGB', reso)
    img.putdata(pixels)
    img.save(fname)
    if DEBUG_MODE:
        print("pixels_2_png: Saved to %d pixels to %s" % (len(pixels), fname))


def png_2_pixels(fname):
    im = Image.open(fname)
    pixel_list = []
    pixels = im.load()
    width, height = im.size
    for row in range(height):
        for col in range(width):
            pixel_list.append(pixels[col, row])
    if DEBUG_MODE:
        print("png_2_pixels: Read %d pixels from %s" % (len(pixel_list), fname))
    return pixel_list
