from enum import Enum
from functools import partial

from PyQt5.QtGui import QPixmap

import utils
from application.tmx_converter import TmxConverter

import PyQt5
import sys

from PyQt5 import uic
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QApplication, QFileDialog, QAction

from tileset_data import TileSetImageData
from tileset_image_not_found_dialog import TilesetImageNotFoundDialogWindow
from ui_constants import FILE_FILTER_TILESET, FILE_FILTER_IMAGE


def show_tileset_image_not_found_dialog(tileset_name, tileset_image_src, main_window):
    dialog_window = TilesetImageNotFoundDialogWindow(tileset_name, tileset_image_src, main_window)
    if dialog_window.exec():
        i = 0
        selected_file = dialog_window.selected_file
        # dialog_window.close()
        return selected_file


def can_generate_tmx(tmx_converter: TmxConverter):
    return tmx_converter.tileset and tmx_converter.tileset_image and tmx_converter.tileset


class MainWindow(PyQt5.QtWidgets.QMainWindow):
    tmx_converter: TmxConverter

    def reset(self, app):
        self.close()
        self.__init__()

    def check_generate_tmx_btn(self):
        if can_generate_tmx(self.tmx_converter):
            self.generate_tmx_btn.setEnabled(True)

    def __init__(self):

        super(MainWindow, self).__init__()
        uic.loadUi('ui/main_window.ui', self)

        self.tmx_converter = TmxConverter()

        self.__disable_conversion_objects__()
        self.__init_file_tool_buttons__()
        self.set_debug_options()

        self.show()

    def __disable_conversion_objects__(self):
        self.tileset_frame.setEnabled(False)
        self.map_image_frame.setEnabled(False)
        self.generate_tmx_btn.setEnabled(False)
        self.normalize_colors_checkbox.setEnabled(False)
        self.layer_transparency_checkbox.setEnabled(False)

    def set_debug_options(self):
        if __debug__:
            action_reset_ui = QAction('Reset UI', self)
            action_reset_ui.setShortcut('Ctrl+R')
            action_reset_ui.triggered.connect(self.reset)
            self.menuFile.addAction(action_reset_ui)
            self.menuFile.setTitle('File (Debug)')

    def __init_file_tool_buttons__(self):
        self.tsx_file_tool_btn.clicked.connect(self.load_tsx)
        # self.tileset_image_file_tool_btn.clicked.connect(partial(select_file, FILE_FILTER_IMAGE))
        self.map_file_tool_btn.clicked.connect(self.load_map_image)

    def load_tsx(self):
        selected_file = utils.select_file(FILE_FILTER_TILESET)

        if self.tmx_converter.load_tileset(selected_file):
            self.set_tsx_view(selected_file)

            source_folder = selected_file[0:selected_file.rindex('/')]

            try:
                tileset_image_loaded = self.tmx_converter.load_tileset_image(source_folder)
                if tileset_image_loaded:
                    self.set_tile_image_view(source_folder)
            except FileNotFoundError as err:
                selected_file = show_tileset_image_not_found_dialog(self.tmx_converter.tileset.name,
                                                                    self.tmx_converter.tileset.image_data.source, self)
                if selected_file is not None and self.tmx_converter.load_tileset_image_fullpath(selected_file):
                    self.set_tile_image_view(source_folder)

            self.check_generate_tmx_btn()
            return True

        return False

    def set_tsx_view(self, selected_file):
        self.tsx_file_name_edit.setText(selected_file)
        self.tileset_frame.setEnabled(True)
        tileset_variable_dict = vars(self.tmx_converter.tileset)
        for item in tileset_variable_dict:
            grid_object = self.__getattribute__(str(item + '_value'))
            grid_object.setText(str(tileset_variable_dict[item]))

    # todo;
    def load_tileset_image(self):

        if self.tmx_converter.tileset_image:
            # show "tileset_already_loaded_prompt"
            pass

        selected_file = utils.select_file(FILE_FILTER_IMAGE)

    def set_tile_image_view(self, source_folder):
        file_path = source_folder + '/' + self.tmx_converter.tileset.image_data.source
        self.tileset_image_name_edit.setText(file_path)
        tileset_image_pixmap = QPixmap(file_path)
        self.tileset_image_graphic.setPixmap(tileset_image_pixmap)

    def load_map_image(self):
        selected_file = utils.select_file(FILE_FILTER_IMAGE)
        try:
            if self.tmx_converter.load_map_image(selected_file):
                self.set_map_image_view(selected_file)
        # todo; exception logic
        except:
            pass

    def set_map_image_view(self, selected_file):
        self.map_file_name_edit.setText(selected_file)
        self.map_image_frame.setEnabled(True)

        map_image_variable_dict = vars(self.tmx_converter.map_image)
        main_window_vars = vars(self)

        file_name = selected_file[selected_file.rindex('/'):]
        self.map_image_name_value.setText(file_name)
        for item in map_image_variable_dict:
            name = str('map_' + item + '_value')
            grid_object = main_window_vars.get(name, None)
            if grid_object is not None:
                grid_object.setText(str(map_image_variable_dict[item]))

        self.map_image_graphic.setText('')
        map_pixmap = QPixmap(selected_file)
        self.map_image_graphic.setPixmap(map_pixmap)
