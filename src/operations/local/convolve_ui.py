from numpy import array
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSpinBox
from PyQt5.QtCore import Qt, QMetaObject
from PyQt5.QtGui import QIcon, QPixmap

from ..operation_ui import OperationUI
from .local_ui import LocalUI


class ConvolveUI(OperationUI, LocalUI):
    """Build UI for :class:`convolve.Convolve`."""

    def init_ui(self, convolve):
        """
        Create user interface for :class:`convolve.Convolve`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param convolve: The dialog convolve window
        :type convolve: :class:`convolve.Convolve`
        """

        self.operation_ui(self)
        self.local_ui(self)
        convolve.setObjectName("convolve")
        self.kernel_values = array([[1] * 3, [1] * 3, [1] * 3])

        icon = QIcon()
        icon.addPixmap(QPixmap("icons/matrix.png"), QIcon.Normal, QIcon.Off)
        convolve.setWindowIcon(icon)

        self.label_kernel_size.setVisible(False)
        self.sb_kernel_size.setVisible(False)

        self.layout_form.addRow(self.label_border_type, self.cb_border_type)

        self.label_kernel = QLabel(convolve)
        self.label_kernel.setAlignment(Qt.AlignCenter)
        self.label_kernel.setObjectName("label_kernel")

        self.layout_grid = QVBoxLayout(convolve)
        self.layout_grid.setObjectName("layout_grid")

        for i in range(3):
            layout_column = QHBoxLayout()

            for j in range(3):
                sb_kernel_cell = QSpinBox()
                sb_kernel_cell.setMinimum(-100)
                sb_kernel_cell.setMaximum(100)
                sb_kernel_cell.setAlignment(Qt.AlignCenter)

                sb_kernel_cell.setValue(self.kernel_values[i][j])
                sb_kernel_cell.valueChanged.connect(
                    lambda value, index=(i, j): convolve.update_kernel_value(index, value)
                )

                layout_column.addWidget(sb_kernel_cell)

            widget = QWidget()
            widget.setLayout(layout_column)
            self.layout_grid.addWidget(widget)

        self.grid = QWidget()
        self.grid.setLayout(self.layout_grid)
        self.grid.setObjectName("grid")

        self.layout.addWidget(self.form)
        self.layout.addWidget(self.label_kernel)
        self.layout.addWidget(self.grid)
        self.layout.addWidget(self.label_image)
        self.layout.addWidget(self.button_box)

        convolve.setLayout(self.layout)
        QMetaObject.connectSlotsByName(convolve)
