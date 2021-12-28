import PyQt5
from PyQt5 import uic
from ui_constants import FILE_FILTER_TILESET, FILE_FILTER_IMAGE

import utils

TILESET_IMAGE_SRC_KEY = '%TILESET_IMAGE_SRC%'
TILESET_FILE_NAME_KEY = '%TILESET_FILE_NAME%'


class TilesetImageNotFoundDialogWindow(PyQt5.QtWidgets.QDialog):

    selected_file: str = None
    canceled: bool = False

    def _accept(self):
        self.selected_file = utils.select_file(FILE_FILTER_IMAGE)
        self.close()
        self.accept()

    def _reject(self):
       # self.close()
        self.reject()

    def __init__(self, tileset_name, tileset_image_src, main_window):
        super(TilesetImageNotFoundDialogWindow, self).__init__()
        uic.loadUi('ui/tileset_image_not_found_dialog.ui', self)

        message_text = self.message.text().replace(TILESET_IMAGE_SRC_KEY, tileset_image_src)
        message_text = message_text.replace(TILESET_FILE_NAME_KEY, tileset_name)

        self.message.setText(message_text)
        self.buttonBox.accepted.connect(self._accept)
        self.buttonBox.rejected.connect(self._reject)

        # self.show()
        self.setFocus()
