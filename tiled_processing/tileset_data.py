class TileSetImageData:

    def __init__(self, source, width, height):
        self.source = source
        self.width = width
        self.height = height

    source: str
    width: int
    height: int

    def __str__(self):
        return self.source


class TileSetData:

    def __init__(self, name, width, height, count, columns, image_data, spacing, margin):
        self.name = name
        self.tile_width = width
        self.tile_height = height
        self.tile_count = count
        self.columns = columns
        self.image_data = image_data
        self.spacing = spacing
        self.margin = margin

    name: str
    tile_width: int
    tile_height: int
    tile_count: int
    columns: int
    spacing: int
    margin: int
    image_data: TileSetImageData

    def __str__(self):
        return self.name
