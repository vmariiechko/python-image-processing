from numpy import array
from PyQt5.QtWidgets import QWidget, QLabel, QSpinBox, QRadioButton, QHBoxLayout, QVBoxLayout
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
        self.kernel1_values = array([[1] * 3, [1] * 3, [1] * 3])
        self.kernel2_values = array([[1] * 3, [1] * 3, [1] * 3])

        icon = QIcon()
        icon.addPixmap(QPixmap("icons/matrix.png"), QIcon.Normal, QIcon.Off)
        convolve.setWindowIcon(icon)

        self.label_kernel_size.setVisible(False)
        self.sb_kernel_size.setVisible(False)

        self.label_two_stage_convolve = QLabel(convolve)
        self.label_two_stage_convolve.setObjectName("label_two_stage_convolve")

        self.rbtn_two_stage_convolve = QRadioButton()
        self.rbtn_two_stage_convolve.setObjectName("rbtn_two_stage_convolve")

        self.layout_form.addRow(self.label_two_stage_convolve, self.rbtn_two_stage_convolve)
        self.layout_form.addRow(self.label_border_type, self.cb_border_type)

        self.label_kernel = QLabel(convolve)
        self.label_kernel.setAlignment(Qt.AlignCenter)
        self.label_kernel.setObjectName("label_kernel")

        self.layout_kernels = QHBoxLayout()
        self.layout_kernels.setObjectName("layout_kernels")

        self.layout_grid1 = self.create_layout_grid(convolve, True)
        self.layout_grid2 = self.create_layout_grid(convolve, False)

        self.grids = [QWidget(), QWidget()]
        self.grids[0].setLayout(self.layout_grid1)
        self.grids[1].setLayout(self.layout_grid2)
        self.grids[1].setVisible(False)

        self.label_grid5x5 = QLabel(convolve)
        self.label_grid5x5.setAlignment(Qt.AlignCenter)
        self.label_grid5x5.setVisible(False)
        self.label_grid5x5.setObjectName("label_grid5x5")

        self.layout_kernels.addWidget(self.grids[0])
        self.layout_kernels.addWidget(self.label_grid5x5)
        self.layout_kernels.addWidget(self.grids[1])

        self.kernels_widget = QWidget(convolve)
        self.kernels_widget.setObjectName("kernels_widget")
        self.kernels_widget.setLayout(self.layout_kernels)

        self.layout.addWidget(self.form)
        self.layout.addWidget(self.label_kernel)
        self.layout.addWidget(self.kernels_widget)
        self.layout.addWidget(self.show_hist_widget)
        self.layout.addWidget(self.preview_widget)
        self.layout.addWidget(self.button_box)

        convolve.setLayout(self.layout)
        QMetaObject.connectSlotsByName(convolve)

    def create_layout_grid(self, convolve, first_kernel):
        """
        Create layout grid 3x3 of spin boxes to input kernel values.

        :param convolve: The dialog convolve window
        :type convolve: :class:`convolve.Convolve`
        :param first_kernel: The flag to indicate whether the layout is for first or second kernel
        :return: bool
        """

        layout_grid = QVBoxLayout()

        for i in range(3):
            layout_column = QHBoxLayout()

            for j in range(3):
                sb_kernel_cell = QSpinBox()
                sb_kernel_cell.setMinimum(-100)
                sb_kernel_cell.setMaximum(100)
                sb_kernel_cell.setAlignment(Qt.AlignCenter)

                if first_kernel:
                    sb_kernel_cell.setValue(self.kernel1_values[i][j])
                else:
                    sb_kernel_cell.setValue(self.kernel2_values[i][j])

                sb_kernel_cell.valueChanged.connect(
                    lambda value, index=(i, j), first=first_kernel: convolve.update_kernel_value(index, value, first)
                )

                layout_column.addWidget(sb_kernel_cell)

            widget = QWidget()
            widget.setLayout(layout_column)
            layout_grid.addWidget(widget)

        return layout_grid
