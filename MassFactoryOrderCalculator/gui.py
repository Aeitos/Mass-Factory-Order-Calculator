#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
:Module author: Cédric Malet <cedric.malet.art@gmail.com>

GUI module using PyQT5 to create interface for the Mass Factory Order Calculator.
"""
from PyQt5 import QtWidgets
from . import core


class MassFactoryUI(QtWidgets.QWidget):
    """
    Instance for the UI.
    """

    def __init__(self):
        super().__init__()

        self.build_ui()
        self.make_connection()
        self.display_info()

    def build_ui(self):
        """
        Build the UI using Qt Layouts and Widgets.
        """
        # Main Layouts
        self.main_layout = QtWidgets.QHBoxLayout(self)

        # === List Widget ===
        # Layout
        self.list_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.list_layout)

        # = Search Bar =
        # Create Widget
        self.search_bar_line_edit = QtWidgets.QLineEdit(self)

        # Setup widget
        self.search_bar_line_edit.setPlaceholderText('Search Bar')
        self.search_bar_line_edit.setStyleSheet("color: white;")

        # Add widget to layout
        self.list_layout.addWidget(self.search_bar_line_edit)

        # = List Widget =
        # Create Widget
        self.craft_list_widget = QtWidgets.QListWidget(self)
        self.craft_list_widget.setStyleSheet("color: white;"
                                             "background-color: #404040;")
        # Setup widget
        # Create item_list_widgets in the list_widget.
        self.build_craft_list()

        # Add widget to layout
        self.list_layout.addWidget(self.craft_list_widget)

        # === Info Widget ===
        # Layout
        self.info_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.info_layout)

        # = Info Text Browser =
        # Create Widget
        self.info_text_browser = QtWidgets.QTextBrowser(self)

        # Setup widget
        self.info_text_browser.setStyleSheet("color: white;")

        # Add widget to layout
        self.info_layout.addWidget(self.info_text_browser)

        # = Crate Number Widget =
        # Layout
        self.crate_number_layout = QtWidgets.QHBoxLayout()
        self.info_layout.addLayout(self.crate_number_layout)

        # = Spinbox Widget =
        # Create Widget
        self.crate_number_spinbox = QtWidgets.QSpinBox(self)

        # Setup widget
        self.crate_number_spinbox.setStyleSheet("color: white;")
        self.crate_number_spinbox.setRange(1, 9)
        self.crate_number_spinbox.setValue(9)

        # Add widget to layout
        self.crate_number_layout.addWidget(self.crate_number_spinbox)

        # = Buttons Widget =
        # Create Widget
        self.minus_button = QtWidgets.QPushButton(self, text='-')
        self.plus_button = QtWidgets.QPushButton(self, text='+')

        # Setup widget
        self.minus_button.setStyleSheet("color: white;")
        self.plus_button.setStyleSheet("color: white;")

        # Add widget to layout
        self.crate_number_layout.addWidget(self.plus_button)
        self.crate_number_layout.addWidget(self.minus_button)

    def make_connection(self):
        self.search_bar_line_edit.textChanged.connect(self.refresh_list_widget)
        self.craft_list_widget.itemSelectionChanged.connect(self.display_info)

        self.plus_button.clicked.connect(self.add_crate)
        self.minus_button.clicked.connect(self.remove_crate)

        self.crate_number_spinbox.valueChanged.connect(self.display_info)

    def refresh_list_widget(self):
        self.craft_list_widget.clear()
        filter_craft = self.search_bar_line_edit.text()
        self.build_craft_list(filter_craft)

    def build_craft_list(self, filter_craft=None):
        if not filter_craft:
            use_filter = False
        else:
            use_filter = True
        categories = core.get_categories()
        for category in categories:
            crafts = core.get_crafts(category)
            for craft in crafts:
                if use_filter:
                    if filter_craft.lower() in craft.lower():
                        item_list_widget = QtWidgets.QListWidgetItem(parent=self.craft_list_widget)
                        item_list_widget.setText(craft)
                else:
                    item_list_widget = QtWidgets.QListWidgetItem(parent=self.craft_list_widget)
                    item_list_widget.setText(craft)
        self.craft_list_widget.setCurrentItem(self.craft_list_widget.item(0))

    def display_info(self):
        selected_list_item = self.craft_list_widget.selectedItems()
        if selected_list_item:
            craft = selected_list_item[0].text()
            crate_num = self.crate_number_spinbox.value()
            category = core.get_craft_category(craft)
            if category == 'Vehicle' or category == 'Shippable':
                if crate_num > 5:
                    self.crate_number_spinbox.setValue(5)
                    crate_num = self.crate_number_spinbox.value()
            info_text = core.create_info_text(craft, crate_num)
            self.info_text_browser.setText(info_text)

    def add_crate(self):
        num = self.crate_number_spinbox.value()
        category = core.get_craft_category(self.craft_list_widget.selectedItems()[0].text())
        if not category == 'Vehicle' or 'Shippable':
            if num < 9:
                self.crate_number_spinbox.setValue(num + 1)
        self.display_info()

    def remove_crate(self):
        num = self.crate_number_spinbox.value()
        if num > 1:
            self.crate_number_spinbox.setValue(num - 1)
        self.display_info()
