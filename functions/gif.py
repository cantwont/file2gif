import os
import imageio


def make_gif(parent_folder, fname):
    items = os.listdir(parent_folder)
    png_filenames = []
    for elem in items:
        if elem.find(".png") != -1:
            png_filenames.append(elem)

    sorted_png = []
    while True:
        lowest = 10000000
        lowest_idx = -1
        for p in png_filenames:
            val = int(p.split("-")[1].split(".")[0])
            if lowest_idx == -1 or val < lowest:
                lowest = val
                lowest_idx = png_filenames.index(p)
        sorted_png.append(png_filenames[lowest_idx])
        del png_filenames[lowest_idx]
        if len(png_filenames) == 0: break
    png_filenames = sorted_png

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, fname + ".gif")
    with imageio.get_writer(output_path, mode='I', duration=0.1) as writer:
        for filename in png_filenames:
            image = imageio.imread(parent_folder + "/" + filename)
            writer.append_data(image)
    return output_path
