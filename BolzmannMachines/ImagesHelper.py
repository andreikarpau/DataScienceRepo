import numpy as np
import matplotlib.pyplot as plt


class ImagesHelper:

    def __init__(self):
        pass

    @staticmethod
    def get_bit_mask_from_bitmap(image):
        PIXEL_COLOR_LIMIT = 10
        pixels = image.load()
        bitMask = np.zeros(image.size[0] * image.size[1])

        for i in range(0, image.size[0]):
            for j in range(0, image.size[1]):
                pixel = pixels[j, i]

                if (isinstance(pixel, int)):
                    if PIXEL_COLOR_LIMIT < pixel:
                        bitMask[i * image.size[1] + j] = 1

                    continue;


                if (PIXEL_COLOR_LIMIT < pixel[0] or PIXEL_COLOR_LIMIT < pixel[1] or PIXEL_COLOR_LIMIT < pixel[2]):
                    bitMask[i * image.size[1] + j] = 1

        return bitMask

    @staticmethod
    def plot_bit_mask(bit_mask, width, height):
        image = np.asarray(bit_mask).reshape(width, height)

        figure = plt.figure()
        subplot = figure.add_subplot(111)
        subplot.imshow(image, cmap='Greys_r')
        plt.show()

    @staticmethod
    def subplot_bit_mask(bit_mask, width, height, subplot_args, show_plot = False):
        image = np.asarray(bit_mask).reshape(width, height)

        plt.subplot(subplot_args)
        plt.imshow(image, cmap='Greys_r')

        if show_plot:
            plt.show()

