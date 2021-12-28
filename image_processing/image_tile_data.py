class ImageTileData:

    def __init__(self, image_data, unique_tiles, tile_images, rows_count, columns_count):
        self.image_data = image_data
        self.unique_tiles = unique_tiles
        self.unique_tiles_count = len(unique_tiles)
        self.tile_images = tile_images
        self.rows_count = rows_count
        self.columns_count = columns_count
        self.tile_width = tile_images[0][0].width
        self.tile_height = tile_images[0][0].height
        self.image_width = len(image_data)
        self.image_height = len(image_data[0])

    unique_tiles: {}
    image_data: [[]]
    tile_images: [[]]
    rows_count: int
    columns_count: int
    tile_width: int
    tile_height: int

    def get_linear_index(self, x, y):
        return ((x * self.columns_count) + y) + 1

    def get_tile(self, x, y):
        return self.tile_images[x][y]

    def get_volume(self):
        return self.rows_count * self.columns_count
