from image_tile_data import ImageTileData
from tiled_processing import tsx_loader
from tileset_data import TileSetData
from tile_image_processor import get_image_tile_data_from_tsx, get_image_tile_data_from_tsx_fullpath, get_image_tile_data
from traceback import print_exc


class TmxConverter:
    tileset: TileSetData = None
    map_image: ImageTileData = None
    tileset_image: ImageTileData = None

    # settings

    layer_by_transparency: bool = False
    normalize_colors: bool = False

    def load_tileset(self, file_path: str):
        try:
            self.tileset = tsx_loader.parse_tsx_file(file_path)
            return True
        # todo; exception logic
        except:
            pass
        return False

    def load_tileset_image(self, resources_folder: str = None):
        self.tileset_image = get_image_tile_data_from_tsx(self.tileset, resources_folder)
        return self.tileset_image is not None

    def load_tileset_image_fullpath(self, file_path: str):
        self.tileset_image = get_image_tile_data_from_tsx_fullpath(self.tileset, file_path)
        return self.tileset_image is not None
        
    def load_map_image(self, file_path: str):
        tile_width = self.tileset.tile_width
        tile_height = self.tileset.tile_height
        self.map_image = get_image_tile_data(file_path, tile_width, tile_height)
        return self.map_image is not None

