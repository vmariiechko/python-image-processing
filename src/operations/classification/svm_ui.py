from PyQt5.QtWidgets import QLabel, QRadioButton, QSizePolicy
from PyQt5.QtCore import Qt, QMetaObject
from PyQt5.QtGui import QIcon, QPixmap

from ..operation_ui import OperationUI
from ..form_ui import FormUI


class SVMUI(OperationUI, FormUI):
    """Build UI for :class:`svm.SVM`."""

    def init_ui(self, svm):
        """
        Create user interface for :class:`svm.SVM`.

        The method creates the widget objects in the proper containers
        and assigns the object names to them.

        :param svm: The dialog SVM classification window
        :type svm: :class:`svm.SVM`
        """

        self.operation_ui(self)
        self.form_ui(self)
        svm.setObjectName("svm")

        icon = QIcon()
        icon.addPixmap(QPixmap("icons/svm.png"), QIcon.Normal, QIcon.Off)
        svm.setWindowIcon(icon)

        self.rbtn_show_hist.setVisible(False)

        self.label_svm_desc = QLabel(svm)
        self.label_svm_desc.setAlignment(Qt.AlignCenter)
        self.label_svm_desc.setObjectName("label_svm_desc")

        self.label_training_data = QLabel(svm)
        self.label_training_data.setAlignment(Qt.AlignCenter)
        self.label_training_data.setObjectName("label_training_data")

        self.label_svm_accuracy = QLabel(svm)
        self.label_svm_accuracy.setAlignment(Qt.AlignCenter)
        self.label_svm_accuracy.setObjectName("label_svm_accuracy")

        self.label_objects_colors = QLabel(svm)
        self.label_objects_colors.setAlignment(Qt.AlignCenter)
        self.label_objects_colors.setObjectName("label_objects_colors")

        self.rbtn_show_confusion_matrix = QRadioButton("Show Confusion Matrix")
        self.rbtn_show_confusion_matrix.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.rbtn_show_confusion_matrix.setObjectName("rbtn_show_confusion_matrix")

        self.layout_form.addRow(self.rbtn_show_confusion_matrix)

        self.layout.addWidget(self.label_svm_desc)
        self.layout.addWidget(self.label_training_data)
        self.layout.addWidget(self.label_svm_accuracy)
        self.layout.addWidget(self.label_objects_colors)
        self.layout.addWidget(self.form)
        self.layout.addWidget(self.preview_widget)
        self.layout.addWidget(self.button_box)

        svm.setLayout(self.layout)
        QMetaObject.connectSlotsByName(svm)
