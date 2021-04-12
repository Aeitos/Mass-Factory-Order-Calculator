#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
:Module author: Cédric Malet <cedric.malet.art@gmail.com>

GUI module using PyQT5 to create interface for the Mass Factory Order Calculator.
"""
from PyQt5 import QtWidgets, QtGui, QtCore
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
        self.search_bar_line_edit.setFixedWidth(250)

        # Add widget to layout
        self.list_layout.addWidget(self.search_bar_line_edit)

        # = Tab Widget =
        # Create Tab widget
        self.categories_tab_widget = QtWidgets.QTabWidget(self)

        # Add Tab for each category
        for cat in core.get_categories():
            self.create_category_tab_widget(cat)

        # Setup widget
        self.categories_tab_widget.setIconSize(QtCore.QSize(48, 48))
        self.categories_tab_widget.setUsesScrollButtons(False)

        width = self.categories_tab_widget.sizeHint().width()
        self.categories_tab_widget.setFixedWidth(width)
        for index in range(self.categories_tab_widget.count()):
            widget = self.categories_tab_widget.widget(index)
            widget.setFixedWidth(width)


        # Add Tab widget to list layout
        self.list_layout.addWidget(self.categories_tab_widget)

        # === Info Widget ===
        # Layout
        self.info_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.info_layout)

        # = Info Text Browser =
        # Create Widget

        self.craft_label_layout = QtWidgets.QVBoxLayout()
        self.info_layout.addLayout(self.craft_label_layout)

        self.resource_label_layout = QtWidgets.QVBoxLayout()
        self.info_layout.addLayout(self.resource_label_layout)

        self.time_label_layout = QtWidgets.QVBoxLayout()
        self.info_layout.addLayout(self.time_label_layout)

        # Setup widget

        # Add widget to layout

        # = Crate Number Widget =
        # Layout
        self.crate_number_layout = QtWidgets.QHBoxLayout()
        self.info_layout.addLayout(self.crate_number_layout)

        # = Spinbox Widget =
        # Create Widget
        self.crate_number_spinbox = QtWidgets.QSpinBox(self)

        # Setup widget
        self.crate_number_spinbox.setStyleSheet("color: white;")
        self.crate_number_spinbox.setAlignment(QtCore.Qt.AlignCenter)
        self.crate_number_spinbox.setRange(1, 9)
        self.crate_number_spinbox.setValue(9)
        self.crate_number_spinbox.setButtonSymbols(self.crate_number_spinbox.NoButtons)
        self.crate_number_spinbox.setFixedWidth(20)

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

        current_list_widget = self.categories_tab_widget.currentWidget()
        current_list_widget.setCurrentItem(current_list_widget.item(0))



    def make_connection(self):
        self.search_bar_line_edit.textChanged.connect(self.refresh_list_widget)

        self.categories_tab_widget.currentChanged.connect(self.on_switch_tab)

        self.plus_button.clicked.connect(self.add_crate)
        self.minus_button.clicked.connect(self.remove_crate)

        self.crate_number_spinbox.valueChanged.connect(self.display_info)

    def create_category_tab_widget(self, category):

        # = List Widget =
        # Create Widget
        self.craft_list_widget = QtWidgets.QListWidget()

        # Setup widget
        self.craft_list_widget.setStyleSheet("""
        color: white;                              
        border-width: 1px;                             
        border-style: solid;                           
        border-color: black;
        """)
        self.craft_list_widget.setIconSize(QtCore.QSize(36, 36))

        # Create item_list_widgets in the list_widget.
        self.build_craft_list(category, self.craft_list_widget)

        # Set the selection to the first item.
        # self.craft_list_widget.setCurrentItem(self.craft_list_widget.item(0))

        # Make the connection for the display info
        self.craft_list_widget.itemSelectionChanged.connect(self.display_info)

        # = Tab Item Widget =
        # Create QIcon
        category_icon = QtGui.QIcon(core.get_category_icon(category))

        # Setup tab widget.
        index = self.categories_tab_widget.addTab(self.craft_list_widget, category)
        self.categories_tab_widget.setTabIcon(index, category_icon)
        tab_bar = self.categories_tab_widget.tabBar()
        tab_bar.setStyleSheet("""QTabBar::tab {  
            background: #505050;                         
            color: white;                              
            border-width: 1px;                             
            border-style: solid;                           
            border-color: black;                             
            border-top-left-radius: 2px;                   
            border-top-right-radius: 2px;                  
            min-height: 50px;                              
        }                                                  
        QTabBar::tab:selected {                            
            border-color: lightgray;                             
        }                                                  
        QTabBar::tab:!selected {                           
            margin-top: 2px;                               
        }                          """)

    def build_craft_list(self, category, list_widget):
        crafts = core.get_crafts(category)
        for craft in crafts:
            item_list_widget = QtWidgets.QListWidgetItem(parent=list_widget)
            item_list_widget.setText(craft)
            craft_icon = QtGui.QIcon(core.get_craft_icon(craft))
            item_list_widget.setIcon(craft_icon)

    def refresh_list_widget(self):
        """
        Rebuild current list widget with filter.
        """

        # Get current category
        category = self.categories_tab_widget.tabText(self.categories_tab_widget.currentIndex())

        # Get current list widget
        list_widget = self.categories_tab_widget.currentWidget()

        # Clear current list widget
        list_widget.clear()

        # Get the filter str.
        filter_craft = self.search_bar_line_edit.text()

        # Create list item widget.
        self.rebuild_craft_list(filter_craft, category, list_widget)

    def rebuild_craft_list(self, filter_craft, category, list_widget):
        """
        Add each craft to de list widget depending if filter is in the craft

        :param str filter_craft: str use to filter item in list widget.
        :param str category: current category filtered
        :param QWidget list_widget: current list widget rebuild.
        """
        # Retrieve list of craft for the category.
        crafts = core.get_crafts(category)
        for craft in crafts:
            if filter_craft.lower() in craft.lower():

                # Create an item list widget.
                item_list_widget = QtWidgets.QListWidgetItem(parent=list_widget)

                # Set the text of the craft.
                item_list_widget.setText(craft)

                # Set craft icon.
                craft_icon = QtGui.QIcon(core.get_craft_icon(craft))
                item_list_widget.setIcon(craft_icon)

    def display_info(self):
        category = self.categories_tab_widget.tabText(self.categories_tab_widget.currentIndex())
        if category == "Vehicles" or category == "Shipable":
            if self.crate_number_spinbox.value() > 5:
                self.crate_number_spinbox.setValue(5)
        self.display_base_info()
        self.display_time_info()
        self.display_resources_info()

    def display_base_info(self):
        for i in reversed(range(self.craft_label_layout.count())):
            layout = self.craft_label_layout.takeAt(i).layout()
            for x in reversed(range(layout.count())):
                layout.takeAt(x).widget().deleteLater()
            layout.deleteLater()

        selected_craft_list = self.categories_tab_widget.currentWidget()
        if selected_craft_list.selectedItems():
            selected_list_item = selected_craft_list.selectedItems()
            craft = selected_list_item[0].text()
            crate_num = self.crate_number_spinbox.value()
            crate_num_info = core.get_base_info(craft, crate_num)

            craft_name_layout = QtWidgets.QHBoxLayout()
            self.craft_label_layout.addLayout(craft_name_layout)
            craft_name_icon_label = QtWidgets.QLabel()
            craft_icon = QtGui.QIcon(core.get_craft_icon(craft))
            craft_pixmap = craft_icon.pixmap(QtCore.QSize(36, 36))
            craft_name_icon_label.setPixmap(craft_pixmap)

            craft_name_text_label = QtWidgets.QLabel()
            craft_name_text_label.setText(craft)
            craft_name_text_label.setStyleSheet("color: white;")
            font = QtGui.QFont()
            font.setPointSize(14)
            craft_name_text_label.setFont(font)

            craft_name_layout.addWidget(craft_name_icon_label)
            craft_name_layout.addWidget(craft_name_text_label)

            crate_num_layout = QtWidgets.QHBoxLayout()
            self.craft_label_layout.addLayout(crate_num_layout)
            crate_name_icon_label = QtWidgets.QLabel()
            crate_icon = QtGui.QIcon(core.get_crate_icon())
            crate_pixmap = crate_icon.pixmap(QtCore.QSize(36, 36))
            crate_name_icon_label.setPixmap(crate_pixmap)

            crate_num_text_label = QtWidgets.QLabel()
            crate_num_text_label.setText("Total craft item: {}".format(crate_num_info))
            crate_num_text_label.setStyleSheet("color: white;")

            crate_num_layout.addWidget(crate_name_icon_label)
            crate_num_layout.addWidget(crate_num_text_label)

    def display_resources_info(self):
        for i in reversed(range(self.resource_label_layout.count())):
            layout = self.resource_label_layout.takeAt(i).layout()
            for x in reversed(range(layout.count())):
                layout.takeAt(x).widget().deleteLater()
            layout.deleteLater()

        selected_craft_list = self.categories_tab_widget.currentWidget()
        if selected_craft_list.selectedItems():
            selected_list_item = selected_craft_list.selectedItems()
            craft = selected_list_item[0].text()
            crate_num = self.crate_number_spinbox.value()
            resources_info = core.convert_resources_info(craft, crate_num)
            for resource in resources_info:
                if resources_info[resource] != 0:
                    resource_layout = QtWidgets.QHBoxLayout()
                    self.resource_label_layout.addLayout(resource_layout)
                    resource_icon = QtGui.QIcon(core.get_resource_icon(resource))
                    resource_pixmap = resource_icon.pixmap(QtCore.QSize(36, 36))
                    resource_text = "{}: {}".format(resource, resources_info[resource])
                    resource_label_widget = QtWidgets.QLabel()
                    resource_label_widget.setText(resource_text)
                    resource_label_widget.setStyleSheet("color: white;")
                    resource_icon_label_widget = QtWidgets.QLabel()
                    resource_icon_label_widget.setPixmap(resource_pixmap)

                    resource_layout.addWidget(resource_icon_label_widget)
                    resource_layout.addWidget(resource_label_widget)

    def display_time_info(self):
        for i in reversed(range(self.time_label_layout.count())):
            layout = self.time_label_layout.takeAt(i).layout()
            for x in reversed(range(layout.count())):
                layout.takeAt(x).widget().deleteLater()
            layout.deleteLater()

        selected_craft_list = self.categories_tab_widget.currentWidget()
        if selected_craft_list.selectedItems():
            selected_list_item = selected_craft_list.selectedItems()
            craft = selected_list_item[0].text()
            crate_num = self.crate_number_spinbox.value()
            time_info = core.convert_time_info(craft, crate_num)
            time_layout = QtWidgets.QHBoxLayout()
            self.time_label_layout.addLayout(time_layout)

            time_icon_label = QtWidgets.QLabel()
            time_icon = QtGui.QIcon(core.get_time_icon())
            time_pixmap = time_icon.pixmap(QtCore.QSize(36, 36))
            time_icon_label.setPixmap(time_pixmap)

            time_text_label = QtWidgets.QLabel()
            time_text_label.setText("Time in seconds: {}".format(time_info))
            time_text_label.setStyleSheet("color: white;")

            time_layout.addWidget(time_icon_label)
            time_layout.addWidget(time_text_label)


    def add_crate(self):
        num = self.crate_number_spinbox.value()
        category = self.categories_tab_widget.tabText(self.categories_tab_widget.currentIndex())
        if not category == 'Vehicle' or 'Shippable':
            if num < 9:
                self.crate_number_spinbox.setValue(num + 1)

    def remove_crate(self):
        num = self.crate_number_spinbox.value()
        if num > 1:
            self.crate_number_spinbox.setValue(num - 1)

    def on_switch_tab(self):
        self.refresh_list_widget()
        current_list_widget = self.categories_tab_widget.currentWidget()
        current_list_widget.setCurrentItem(current_list_widget.item(0))
        self.display_info()
