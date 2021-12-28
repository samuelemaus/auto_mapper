from enum import Enum

from image_tile_data import ImageTileData
from tiled_processing.tileset_data import TileSetData
from tile_image_processor import TileImage
import tile_image_processor
from timeit import default_timer as timer


class EncodingType(Enum):
    CSV = 0
    BASE_64_UNCOMPRESSED = 1
    BASE_64_ZLIB_COMPRESSED = 2
    BASE_64_ZSTANDARD_COMPRESSED = 3


# TODO - multi-threading
# gets the corresponding tileset indices for the matched tiles in the provided map image
def get_tileset_indices(map_image_data: ImageTileData, tileset_image_data: ImageTileData, tileset_data: TileSetData):
    tileset_indices = [-1 for i in range(map_image_data.get_volume())]

    missing_tiles: []

    i = 0
    for row in map_image_data.tile_images:
        for tile in row:
            index = tileset_image_data.unique_tiles.get(tile.get_precomputed_hash(), None)
            if index is not None:
                x, y = index
                linear_index = tileset_image_data.get_linear_index(x, y)
                tileset_indices[i] = linear_index
            i += 1
    return tileset_indices


def convert_img_to_tmx(map_image_file_name: str, tileset_data: TileSetData, resources_folder: str = None):
    tile_width = tileset_data.tile_width
    tile_height = tileset_data.tile_height
    spacing = tileset_data.spacing
    margin = tileset_data.margin

    map_image_data = tile_image_processor.get_image_tile_data(map_image_file_name, tile_width, tile_height, spacing,
                                                              margin, resources_folder)
    tileset_image_data = tile_image_processor.get_image_tile_data(tileset_data.image_data.source, tile_width,
                                                                  tile_height, spacing, margin, resources_folder)

    tileset_indices = get_tileset_indices(map_image_data, tileset_image_data, tileset_data)

    index_str = ""

    # for i, index in enumerate(tileset_indices):
    #     index_str += str(index)
    #
    #     if i < (len(tileset_indices) - 1):
    #         index_str += ","

    # print(index_str)
