from functools import partial
from traceback import print_exc

from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

import tile_image_processor
import tiled_processing.tsx_loader
import tiled_processing.tmx_processor
import tests.threading_tests
import tmx_processor
import tsx_loader
from image_processing import offset_processor
from timeit import default_timer as timer

REBOOT_EXIT_CODE = -999


def reset_ui(app, window):
    app.setQuitOnLastWindowClosed(False)
    window.close()
    window = MainWindow()

    # app.setQuitOnLastWindowClosed(True)


def main():
    app = QApplication([])
    window = MainWindow()
    app.setQuitOnLastWindowClosed(False)
    # window.actionReset_UI.triggered.connect(partial(reset_ui, app, window))
    app.exec()


if __name__ == '__main__':
    main()
