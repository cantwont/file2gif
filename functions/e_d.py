from functions.file import *
from functions.image import *
from functions.header import *
from functions.gif import *
from functions.settings import DEBUG_MODE
import os


def test_bit_similarity(bits1, bits2):
    f = open("bits.txt", "w")
    for b1 in bits1:
        f.write(b1)
    f.write("\n")
    for b2 in bits2:
        f.write(b2)
    f.write("\n")
    f.close()

    if len(bits1) != len(bits2):
        if DEBUG_MODE:
            print("Bit lengths are not the same!")
        return
    for b1, b2 in zip(bits1, bits2):
        if b1 != b2:
            if DEBUG_MODE:
                print("Bits are not the same!")
            return
    if DEBUG_MODE:
        print("Bits are identical")


def encode(src, res=four_k):
    bits = file_2_bits(src)
    bits = add_header(bits, src.split("/")[-1])
    pixels = bits_2_pixels(bits)

    pixels_per_image = res[0] * res[1]

    num_imgs = int(len(pixels) / pixels_per_image) + 1

    if DEBUG_MODE:
        print("encode: Encoding will require %d .png frames" % num_imgs)

    name_clean = src.split("/")[-1]

    clear_folder("temp")

    for i in range(num_imgs):
        cur_temp_name = "temp/" + name_clean + "-" + str(i) + ".png"
        cur_start_idx = i * pixels_per_image
        cur_span = min(pixels_per_image, len(pixels) - cur_start_idx)
        cur_pixels = pixels[cur_start_idx:cur_start_idx + cur_span]
        pixels_2_png(cur_pixels, cur_temp_name)
        if cur_span < pixels_per_image: break

    gif_name = make_gif("temp", name_clean)
    return gif_name


def decode(src):
    def iter_frames(im):
        try:
            i = 0
            while 1:
                im.seek(i)
                imframe = im.copy()
                imframe = imframe.convert('RGB')
                yield imframe
                i += 1
        except EOFError:
            pass

    im = Image.open(src)

    saved_frames = []
    for i, frame in enumerate(iter_frames(im)):
        cur_frame = "temp/frame-%d.png" % i
        saved_frames.append(cur_frame)
        frame.save(cur_frame, **frame.info)

    if DEBUG_MODE:
        print("decode: Identified %d .png frames" % len(saved_frames))

    pixels = []
    for s in saved_frames:
        cur_pixels = png_2_pixels(s)
        pixels.extend(cur_pixels)

    bits = pixels_2_bits(pixels)

    fname, bits = decode_header(bits)

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, fname.split(".")[0] + "-recovered." + fname.split(".")[1])
    bits_2_file(bits, output_path)
