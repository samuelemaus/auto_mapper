import numpy as np
from image_processing.image_constants import ChannelIndexes, EIGHT_BIT_MAX


class RGBAData:

    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    r: int = 0
    g: int = 0
    b: int = 0
    a: int = 0

    r_sum: int = 0
    g_sum: int = 0
    b_sum: int = 0
    a_sum: int = 0

    def get_total_sum(self):
        return self.r_sum + self.g_sum + self.b_sum


class TileImage:

    def __init__(self, width, height, data=None, compute_hash: bool = True, transparency_color: [] = None):
        self.width = width
        self.height = height
        self.data = data
        if self.data is None:
            self.data = [[[0, 0, 0, 0] for x in range(width)] for y in range(height)]
        self.transparency_color = transparency_color
        if compute_hash:
            self.get_precomputed_hash()

    data: [[]]
    width: int
    height: int
    transparency_color: [] = None
    __is_transparency_layer: bool = None
    __precomputed_hash: int = None

    def _calculate_is_transparency_layer(self):

        def contains_low_alpha(_pixel: []):
            return _pixel[ChannelIndexes.ALPHA.value] < EIGHT_BIT_MAX

        def is_transparency_color(_pixel: []):
            return _pixel == self.transparency_color

        evaluation_function = contains_low_alpha if self.transparency_color is None else is_transparency_color

        for row in self.data:
            for pixel in row:
                if evaluation_function(pixel):
                    return True

        return False

    def get_is_transparency_layer(self):
        if self.__is_transparency_layer is None:
            self.__is_transparency_layer = self._calculate_is_transparency_layer()

        return self.__is_transparency_layer

    def __eq__(self, other):

        return isinstance(other,
                          TileImage) and self.width == other.width and self.height == other.height and np.array_equal(
            self.data, other.data)

    def get_precomputed_hash(self):
        if self.__precomputed_hash is None:
            hash(self)

        return self.__precomputed_hash

    def __hash__(self):
        hash_str = hex(self.width)[2:] + hex(self.height)[2:]
        for x in range(self.height):
            for y in range(self.width):
                pixel = self.data[x][y]
                for color in pixel:
                    hash_str += hex(color)[2:]
        self.__precomputed_hash = hash(hash_str)
        return self.get_precomputed_hash()
