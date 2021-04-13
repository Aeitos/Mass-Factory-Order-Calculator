#!/usr/bin/python3
# -*- coding: utf-8 -*-
from . import gui
from PyQt5 import QtWidgets
import sys

app = QtWidgets.QApplication([])

widget = gui.MassFactoryUI()
widget.setStyleSheet("background-color: #404040;")
widget.resize(460, 400)
widget.show()

sys.exit(app.exec_())
