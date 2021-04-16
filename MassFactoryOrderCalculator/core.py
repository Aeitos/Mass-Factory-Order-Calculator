#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Author
"""

import sys
import os
import json

if getattr(sys, 'frozen', False):
    DIR_PATH = sys._MEIPASS
else:
    DIR_PATH = os.path.dirname(os.path.abspath(__file__))

_JSON_PATH = "{}/ressources/mass_factory_data.json".format(DIR_PATH)

INFO_LIST = ["Unit par crate", "B. Mat", "E. Mat", "H.E. Mat", "R. Mat", "Time (seconds)"]

_RESSOURCES_PATH = "{}/ressources".format(DIR_PATH)


def get_json_data():
    """
    Extract json data from mass_factory_data.json file
    :return:
    """
    with open(_JSON_PATH) as json_access:
        json_data = json.load(json_access)
    return json_data


JSON_DATA = get_json_data()


def get_info(craft_input):
    """
    Get info from specified craft name.

    :param str craft_input: craft name.
    :return dict: Info for specified craft
    """
    for category in JSON_DATA:
        for craft in JSON_DATA[category]:
            if craft == craft_input:
                return JSON_DATA[category][craft]


def convert_resources_info(craft_input, crate_num):
    """
    Convert resource info with specified number of crate.

    :param str craft_input: Craft name.
    :param int crate_num:  Number of crates.
    :return dict: Converted info.
    """

    # Get craft info.
    info = get_info(craft_input)

    # Create output dict.
    converted_info_dict = {}

    # Process for each info.
    for inf in info:

        # Check if info are resources.
        if inf in INFO_LIST[1:5]:

            # Set the first step price reduction.
            reduction = 90

            # Set first value to loop on.
            converted_info_dict[inf] = 0

            # Process for each number of crate.
            for i in range(crate_num):

                # Apply reduction on resource price and add it to the total cost.
                converted_value = converted_info_dict[inf] + int(info[inf] * reduction / 100.0)

                # Check if value not 0, to bypass 0 cost resources.
                if converted_value != 0:
                    converted_info_dict[inf] = converted_value

                # Check reduction state if more than 50 %, reduce it by 10 %.
                if not reduction == 50:
                    reduction -= 10
    return converted_info_dict


def convert_time_info(craft_input, crate_num):
    """
    Convert time info with specified number of crate.

    :param str craft_input: Craft name.
    :param int crate_num: Crate number.
    :return int: Converted time info.
    """

    # Get craft info.
    info = get_info(craft_input)

    # Get time info.
    time_info = info[INFO_LIST[-1]]

    # Convert time info
    converted_info = time_info * crate_num

    return converted_info


def get_base_info(craft_input, crate_num):
    """
    Convert basic info with specified number of crate.

    :param str craft_input: Craft name.
    :param int crate_num: Crate number.
    :return int: Converted basic info.
    """

    # Get craft info.
    info = get_info(craft_input)

    # Get crate info.
    crate_info = info[INFO_LIST[0]]

    # Convert crate info.
    converted_info = crate_info * crate_num

    return converted_info


def get_craft_category(craft_item):
    """
    Retrieve category for a given craft.

    :param str craft_item: Craft name.
    :return str: Category name.
    """
    for category in JSON_DATA:
        if craft_item in JSON_DATA[category]:
            return category


def get_categories():
    """
    Get all categories.
    :return list: All categories in data.
    """
    return [category for category in JSON_DATA]


def get_crafts(category):
    """
    Get all crafts of a given category.

    :param str category: Category name.
    :return list: All crafts of the category.
    """
    return [craft for craft in JSON_DATA[category]]


def get_category_icon(category):
    """
    Get icon associated with the category.

    :param str category: Category name.
    :return path: Path of the icon.
    """
    return "{}/Icons_category/{}.png".format(_RESSOURCES_PATH, category)


def get_craft_icon(craft):
    """
    Get icon associated with the craft.

    :param str craft: Craft name.
    :return path: Path of the icon.
    """

    # Get category of the craft.
    category = get_craft_category(craft)
    return "{}/{}/{}.png".format(_RESSOURCES_PATH, category, craft)


def get_resource_icon(resource):
    """
    Get icon associated with the resource.

    :param str resource: Resource name.
    :return path: Path of the icon.
    """
    return "{}/Ressources/{}".format(_RESSOURCES_PATH, resource)


def get_crate_icon():
    """
    Get the crate icon.

    :return path: Path of the icon.
    """
    return "{}/Ressources/Crate".format(_RESSOURCES_PATH)


def get_time_icon():
    """
    Get the time icon.

    :return path: Path of the icon.
    """
    return "{}/Ressources/Time".format(_RESSOURCES_PATH)
