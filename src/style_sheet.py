from PyQt5 import QtCore


def load_style_sheet():
    """
    Loads style.qss content.

    :return: style sheet for :class:`main.MainWindow`
    :rtype: str
    """

    style = QtCore.QFile(f'style.qss')

    if not style.exists():
        return
    else:
        style.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        text = QtCore.QTextStream(style)
        style_sheet = text.readAll()
        return style_sheet
