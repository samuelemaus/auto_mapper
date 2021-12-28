from xml.dom import minidom
from xml.dom.minidom import Element

import tiled_processing.tiled_constants as keys
from tileset_data import TileSetData, TileSetImageData


def parse_tsx_file(file_name: str) -> TileSetData:
    tsx_file = minidom.parse(file_name)
    tileset_xml_data = tsx_file.getElementsByTagName(keys.TILESET_KEY)[0]
    image_xml_data = tsx_file.getElementsByTagName(keys.IMAGE_KEY)[0]
    return get_tileset_data(tileset_xml_data, image_xml_data)


def get_image_data(image_xml_data: Element) -> TileSetImageData:
    source = _get_attribute(image_xml_data, keys.SOURCE_KEY, str)

    if source.__contains__('/'):
        source = source[source.index('/'):]

    width = _get_attribute(image_xml_data, keys.WIDTH_KEY, int)
    height = _get_attribute(image_xml_data, keys.HEIGHT_KEY, int)

    return TileSetImageData(source, width, height)


def _get_attribute(xml_data: Element, attribute_name: str, target_type: type):
    value = xml_data.getAttribute(attribute_name)
    if value is not '':
        return target_type(value)

    return target_type()


def get_tileset_data(tileset: Element, image_xml_data: Element) -> TileSetData:
    name = _get_attribute(tileset, keys.NAME_KEY, str)
    width = _get_attribute(tileset, keys.TILE_WIDTH_KEY, int)
    height = _get_attribute(tileset, keys.TILE_HEIGHT_KEY, int)
    count = _get_attribute(tileset, keys.TILE_COUNT_KEY, int)
    columns = _get_attribute(tileset, keys.COLUMNS_KEY, int)
    spacing = _get_attribute(tileset, keys.SPACING_KEY, int)
    margin = _get_attribute(tileset, keys.MARGIN_KEY, int)

    image_data = get_image_data(image_xml_data)

    return TileSetData(name, width, height, count, columns, image_data, spacing, margin)
