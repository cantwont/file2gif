from shutil import rmtree
from functions.settings import DEBUG_MODE
import os


def bits_2_file(bits, fname):
    bytes_array = bytearray()
    idx = 0
    inc = 8
    while True:
        char = ''.join(bits[idx:idx + inc])
        bytes_array.append(int(char, 2))
        idx += inc
        if idx >= len(bits):
            break
    with open(fname, 'wb') as f:
        f.write(bytes(bytes_array))

    if DEBUG_MODE:
        print("bits_2_file: Wrote %d bits to %s" % (len(bits), fname))


def file_2_bits(fname):
    bits = []
    try:
        with open(fname, "rb") as f:
            byte = f.read(1)
            while byte:
                cur_bits = bin(int.from_bytes(byte, byteorder='big'))[2:]
                while len(cur_bits) < 8:
                    cur_bits = "0" + cur_bits
                for b in cur_bits:
                    bits.append(b)
                byte = f.read(1)
    except Exception as e:
        if DEBUG_MODE:
            print(f"Error reading file: {e}")

    return bits


def bits_2_pixels(bits):
    pixels = []

    progress_bar_length = 25
    progress_bar_item = "-"
    progress_bar_empty_item = " "

    '''
    for i,b in enumerate(bits):

        num_items = int( float(i)/float(len(bits))*float(progress_bar_length) )
        progress_string = ""
        for prog_index in range(progress_bar_length):
            if prog_index<=num_items:
                progress_string += progress_bar_item
            else:
                progress_string += progress_bar_empty_item
        progress_string += "]"
        print("bits2pixels... ["+progress_string,end="\r")
        sys.stdout.flush()

        if b=='0':
            pixels.append((0,0,0))
        else:
            pixels.append((255,255,255))
    sys.stdout.write("\n")
    '''
    for b in bits:
        pixels.append((0, 0, 0) if b == '0' else (255, 255, 255))
    if DEBUG_MODE:
        print("bits_2_pixels: Converted %d bits to %d pixels" % (len(bits), len(pixels)))
    return pixels


def pixels_2_bits(pixels):
    bits = []
    for p in pixels:
        if p == (0, 0, 0):
            bits.append('0')
        else:
            bits.append('1')
    if DEBUG_MODE:
        print("pixels_2_bits: Converted %d pixels to %d bits" % (len(pixels), len(bits)))
    return bits


def clear_folder(relative_path):
    try:
        rmtree(relative_path)
    except:
        if DEBUG_MODE:
            print("WARNING: Could not locate /temp directory.")

    for i in range(10):
        try:
            os.mkdir(relative_path)
            break
        except:
            continue
