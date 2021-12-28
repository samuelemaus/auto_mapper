from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QFileDialog


def select_file(file_filter: str):
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)
    dlg.setNameFilter(file_filter)
    filename: str = ''

    # todo- do this a less awful way
    while dlg.exec_():
        filename = dlg.selectedFiles()[0]
        try:
            check_file = QFileInfo(filename)
            if check_file.isFile():
                break
        except:
            pass
    return filename

def get_items_in_grid(grid):
    return [grid.itemAtPosition(r, c) for r in range(grid.rowCount()) for c in range(grid.columnCount())]
    #return list(_get_items_in_grid(grid))


def _get_items_in_grid(grid):
    values = [grid.itemAtPosition(r, c) for r in range(grid.rowCount()) for c in range(grid.columnCount())]
    for val in values:
        if val is not None:
            yield val

