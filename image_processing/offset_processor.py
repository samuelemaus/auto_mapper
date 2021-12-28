import threading
from multiprocessing import cpu_count

from tsx_loader import TileSetData
from image_processing.tile_image_processor import get_image_tile_data
from image_processing.tile_image_processor import get_image_tile_data_from_tsx
from image_processing.tile_image_processor import get_tile_indices_unthreaded
from image_processing.tile_image_processor import load_image
from image_processing.tile_image_processor import write_image


def process_image_data_landscape(column, rows_count, image, new_image: [[]], tile_width, tile_height, margin, spacing):
    rows_processed = 0
    for row in range(rows_count):

        x_start = tile_height * rows_processed
        x_stop = tile_height * (rows_processed + 1)

        x_adjusted = margin + (rows_processed * spacing)

        for new_image_x in range(x_start, x_stop):

            y_start = tile_width * column
            y_stop = tile_width * (column + 1)

            y_adjusted = margin + (column * spacing)

            for new_image_y in range(y_start, y_stop):
                new_image[new_image_x][new_image_y] = image[new_image_x + x_adjusted][new_image_y + y_adjusted]

        rows_processed += 1


def _remove_offset_threaded(image, tile_width, tile_height, row_count, columns_count, margin, spacing):
    # todo - make this work differently based on orientation

    new_image_width = tile_width * columns_count
    new_image_height = tile_height * row_count

    new_image = [[[0, 0, 0, 0] for x in range(new_image_width)] for y in range(new_image_height)]

    thread_count = cpu_count()
    passes = 0
    y = 0
    while y < columns_count:
        for thread_num in range(thread_count):
            if y < columns_count:
                next_thread = threading.Thread(target=process_image_data_landscape, args=(y,
                                                                                          row_count, image, new_image,
                                                                                          tile_width, tile_height,
                                                                                          margin,
                                                                                          spacing))
                next_thread.start()
                next_thread.join()
                passes += 1
            y += 1
    return new_image


def remove_offset_from_image(image_name: str, new_image_name: str, destination: str, tile_width, tile_height,
                             margin: int, spacing: int, rows_count=0,
                             columns_count=0, resources_folder: str = None):
    image_to_load = image_name
    if resources_folder is not None:
        image_to_load = resources_folder + '/' + image_to_load

    image = load_image(image_to_load)
    new_image = _remove_offset_threaded(image, tile_width, tile_height, rows_count, columns_count, margin,
                                        spacing)
    write_image(new_image_name, destination, new_image)


def remove_offset_from_tsx_image(tsx_data: TileSetData, new_image_name: str, destination: str,
                                 resources_folder: str = None):
    image_name = ''

    if resources_folder is not None:
        image_name = resources_folder + '/'

    image_name += tsx_data.image_data.source
    tile_width = tsx_data.tile_width
    tile_height = tsx_data.tile_height
    spacing = tsx_data.spacing
    margin = tsx_data.margin
    rows_count = tsx_data.tile_count // tsx_data.columns
    columns_count = tsx_data.columns
    image = load_image(image_name)
    new_image = _remove_offset_threaded(image, tile_width, tile_height, rows_count, columns_count, margin,
                                        spacing)
    write_image(new_image_name, destination, new_image)
