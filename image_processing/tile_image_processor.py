import math
import sys
from enum import Enum

import imageio

import tsx_loader
from tile_image import TileImage
from image_tile_data import ImageTileData
import threading
from multiprocessing import cpu_count

from timeit import default_timer as timer


class Orientation(Enum):
    LANDSCAPE = 0,
    PORTRAIT = 1


def load_image(file_name: str):
    return imageio.imread(file_name)


def write_image(image_name: str, destination: str, image_data):
    uri = destination + '/' + image_name
    imageio.imwrite(uri, image_data, 'png')


def get_tile_image(image, box, transparency_color: [] = None):
    left, top, right, bottom = box

    tile_width = (right - left) + 1
    tile_height = (bottom - top) + 1

    tile_data = [[[0, 0, 0, 0] for x in range(tile_width)] for y in range(tile_height)]

    tile_index = 0
    for i in range(left, right + 1):
        row = image[i][top:bottom + 1]
        tile_data[tile_index] = row
        tile_index += 1

    return TileImage(tile_width, tile_height, tile_data, True, transparency_color)


# returns a two-dimensional array representing the indices of each tile.
# The indices each contain a four integer tuple (left, top, right, bottom)
def get_tile_indices_unthreaded(image_width: int, image_height: int, tile_width: int, tile_height: int,
                                columns_count: int,
                                rows_count: int, spacing: int = 0, margin: int = 0):
    tile_indices: [[]]

    if (image_width % tile_width != 0) or (image_height % tile_height != 0):
        # todo: some error
        pass

    tile_indices = [[0 for y in range(rows_count)] for x in range(columns_count)]

    for x in range(columns_count):
        for y in range(rows_count):
            x_spacing_mod = spacing * x
            y_spacing_mod = spacing * y

            y_start = (y * tile_width) + (margin + y_spacing_mod)
            y_stop = (((y + 1) * tile_width) - 1) + (margin + y_spacing_mod)

            x_start = (x * tile_height) + (margin + x_spacing_mod)
            x_stop = (((x + 1) * tile_height) - 1) + (margin + x_spacing_mod)

            y_range = range(y_start, y_stop)
            x_range = range(x_start, x_stop)

            next_indices = (x_range.start, y_range.start, x_range.stop, y_range.stop)
            tile_indices[x][y] = next_indices

    return tile_indices


def get_tile_indices_threaded(image_width: int, image_height: int, tile_width: int, tile_height: int,
                              columns_count: int,
                              rows_count: int):
    tile_indices: [[]]
    if (image_width % tile_width != 0) or (image_height % tile_height != 0):
        # todo: some error
        pass
    tile_indices = [[0 for y in range(rows_count)] for x in range(columns_count)]
    thread_count = cpu_count()


def process_tile_thread_task_portrait(x: int, columns_count: int, tile_images: [[]], image, tile_indices, unique_tiles):
    for y in range(columns_count):
        tile_image = get_tile_image(image, tile_indices[x][y])
        tile_images[x][y] = tile_image
        unique_tiles[tile_image.get_precomputed_hash()] = (x, y)


def process_tile_thread_task_landscape(y: int, rows_count: int, tile_images: [[]], image, tile_indices, unique_tiles):
    for x in range(rows_count):
        tile_image = get_tile_image(image, tile_indices[x][y])
        tile_images[x][y] = tile_image
        unique_tiles[tile_image.get_precomputed_hash()] = (x, y)


def get_all_tile_images(image, tile_indices, rows_count: int, columns_count: int):
    # TODO - determine ideal method to get tiles based on processor and/or user setting
    return get_tile_images_threaded(image, tile_indices, rows_count, columns_count)


def get_tile_images_threaded_landscape(image, tile_indices, rows_count: int, columns_count: int):
    unique_tiles = {}

    tile_images = [[None for x in tile_indices[0]] for y in tile_indices]

    thread_count = cpu_count()
    y = 0
    while y < columns_count:
        for thread_num in range(thread_count):
            if y < columns_count:
                next_thread = threading.Thread(target=process_tile_thread_task_landscape, args=(
                    y, rows_count, tile_images, image, tile_indices, unique_tiles))
                next_thread.start()
                next_thread.join()
            y += 1

    return tile_images, unique_tiles


def get_tile_images_threaded_portrait(image, tile_indices, rows_count: int, columns_count: int):
    unique_tiles = {}
    tile_images = [[None for x in tile_indices[0]] for y in tile_indices]

    thread_count = cpu_count()
    x = 0
    while x < rows_count:
        for thread_num in range(thread_count):
            if x < rows_count:
                next_thread = threading.Thread(target=process_tile_thread_task_portrait, args=(
                    x, columns_count, tile_images, image, tile_indices, unique_tiles))
                next_thread.start()
                next_thread.join()
            x += 1

    return tile_images, unique_tiles


def get_tile_images_threaded(image, tile_indices, rows_count: int, columns_count: int):
    # To my surprise, it was measurably faster when testing to break out the methods like this vs. parameterizing
    # the row / column indexes based on orientation in a single method.
    if rows_count > columns_count:
        return get_tile_images_threaded_portrait(image, tile_indices, rows_count, columns_count)

    return get_tile_images_threaded_landscape(image, tile_indices, rows_count, columns_count)


def get_tile_images_unthreaded(image, tile_indices, rows_count: int, columns_count: int):
    tile_images = [[None for x in tile_indices[0]] for y in tile_indices]
    for x in range(rows_count):
        for y in range(columns_count):
            tile_images[x][y] = get_tile_image(image, tile_indices[x][y])
    return tile_images


def get_image_tile_data(image_name: str, tile_width: int, tile_height: int, spacing: int = 0, margin: int = 0,
                        resources_folder: str = None,
                        rows_count: int = 0,
                        columns_count: int = 0):
    image_to_load = image_name
    if resources_folder is not None:
        image_to_load = resources_folder + '/' + image_to_load
    image = load_image(image_to_load)
    image_height = image.shape[0]
    image_width = image.shape[1]

    if rows_count == 0:
        rows_count = (image_height - (margin * 2)) // tile_height + spacing
    if columns_count == 0:
        columns_count = (image_width - (margin * 2)) // tile_width + spacing

    tile_indices = get_tile_indices_unthreaded(image_width, image_height, tile_width, tile_height, rows_count,
                                               columns_count, spacing, margin)
    all_tile_images, unique_tiles = get_all_tile_images(image, tile_indices, rows_count, columns_count)
    return ImageTileData(image, unique_tiles, all_tile_images, rows_count, columns_count)


def get_image_tile_data_from_tsx(tsx_data: tsx_loader.TileSetData, resources_folder: str = None):
    image_name = ''

    # if resources_folder is not None:
    #     image_name = resources_folder + '/'

    image_name += tsx_data.image_data.source
    tile_width = tsx_data.tile_width
    tile_height = tsx_data.tile_height
    spacing = tsx_data.spacing
    margin = tsx_data.margin
    rows_count = tsx_data.tile_count // tsx_data.columns
    columns_count = tsx_data.columns
    return get_image_tile_data(image_name, tile_width, tile_height, spacing, margin, resources_folder, rows_count,
                               columns_count)


def get_image_tile_data_from_tsx_fullpath(tsx_data: tsx_loader.TileSetData, file_path: str):
    tile_width = tsx_data.tile_width
    tile_height = tsx_data.tile_height
    spacing = tsx_data.spacing
    margin = tsx_data.margin
    rows_count = tsx_data.tile_count // tsx_data.columns
    columns_count = tsx_data.columns
    return get_image_tile_data(file_path, tile_width, tile_height, spacing, margin, None, rows_count,
                               columns_count)
