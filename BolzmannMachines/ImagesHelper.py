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
                pixel = pixels[i, j]

                if (PIXEL_COLOR_LIMIT < pixel[0] or PIXEL_COLOR_LIMIT < pixel[1] or PIXEL_COLOR_LIMIT < pixel[2]):
                    bitMask[i * image.size[1] + j] = 1

        return bitMask

    @staticmethod
    def plot_bit_mask(bitMask, width, height):
        image = np.asarray(bitMask).reshape(width, height)
        plt.subplot(441)
        plt.imshow(image)


