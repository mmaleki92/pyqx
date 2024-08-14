#!/usr/bin/env python
# coding: utf-8

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDrag, QColor

class CurrentColor(QtWidgets.QLabel):
    def __init__(self, primary, context, signals, Parent=None):
        super().__init__(Parent)
        self.context = context
        self.signals = signals
        self.primary = primary
        self.color = self.context.primaryColor if primary else self.context.secondaryColor
        self.setObjectName("PrimaryColor" if primary else "SecondaryColor")
        self.setStyleSheet(f"background-color: {self.color.name()};")
        self.setFixedHeight(24)
        self.signals.updateColor.connect(self.updateColor)

    def mouseMoveEvent(self, e):
        mime_data = QtCore.QMimeData()
        mime_data.setColorData(self.color)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        drag.start(QtCore.Qt.MoveAction)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            color = QtWidgets.QColorDialog.getColor(self.color)
            if color.isValid():
                self.context.changePrimaryColor(color) if self.primary else self.context.changeSecondaryColor(color)

    def updateColor(self):
        self.color = self.context.primaryColor if self.primary else self.context.secondaryColor
        self.setStyleSheet(f"background-color: {self.color.name()};")
        super().update()

class Color(QtWidgets.QFrame):
    def __init__(self, position, color, context, signals, Parent=None):
        super().__init__(Parent)
        self.context = context
        self.position = position
        self.color = QColor(*color)
        self.setObjectName("Color")
        self.setFixedSize(12, 12)
        self.setStyleSheet(f"background-color: {self.color.name()};")
        self.setAcceptDrops(True)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.context.changePrimaryColor(self.color)
        elif e.button() == Qt.RightButton:
            self.context.changeSecondaryColor(self.color)
        elif e.button() == Qt.MidButton:
            color = QtWidgets.QColorDialog.getColor(self.color)
            if color.isValid():
                self.changeColor(color)

    def dragEnterEvent(self, e):
        if e.mimeData().hasColor():
            e.accept()

    def dropEvent(self, e):
        self.changeColor(QColor(e.mimeData().colorData()))
        e.accept()

    def update(self):
        self.setStyleSheet(f"background-color: {self.color.name()};")
        super().update()

    def changeColor(self, color):
        self.color = color
        self.context.palette[self.position] = [color.red(), color.green(), color.blue()]
        self.update()

class Palette(QtWidgets.QWidget):
    def __init__(self, context, signals, Parent=None):
        super().__init__(Parent)
        self.context = context

        grid_layout = QtWidgets.QGridLayout()
        for i in range(5):
            for j in range(12):
                grid_layout.addWidget(Color(i * 12 + j, context.palette[i * 12 + j], context, signals), i, j)
        grid_layout.setSpacing(1)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(CurrentColor(True, context, signals))
        hbox.addWidget(CurrentColor(False, context, signals))
        hbox.setSpacing(2)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(grid_layout)
        vbox.setSpacing(2)

        self.setLayout(vbox)
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
