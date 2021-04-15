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

_JSON_PATH = "{}/ressources/data.json".format(DIR_PATH)

INFO_LIST = ["Unit par crate", "B. Mat", "E. Mat", "H.E. Mat", "R. Mat", "Time (seconds)"]

_RESSOURCES_PATH = "{}/ressources".format(DIR_PATH)


def get_json_data():
    """
    Extract json datas from data.json file
    :return:
    """
    with open(_JSON_PATH) as json_access:
        json_data = json.load(json_access)
    return json_data


JSON_DATA = get_json_data()


def get_info(craft_input):
    for category in JSON_DATA:
        for craft in JSON_DATA[category]:
            if craft == craft_input:
                return JSON_DATA[category][craft]


def convert_resources_info(craft_input, crate_num):
    info = get_info(craft_input)
    converted_info_dict = {}
    for inf in info:
        if inf in INFO_LIST[1:5]:
            reduction = 90
            converted_info_dict[inf] = 0
            for i in range(crate_num):
                converted_value = converted_info_dict[inf] + int(info[inf] * reduction / 100.0)
                if converted_value != 0:
                    converted_info_dict[inf] = converted_value
                if not reduction == 50:
                    reduction -= 10
    return converted_info_dict


def convert_info(craft_input, crate_num):
    info = get_info(craft_input)
    converted_info_dict = {}
    for inf in info:
        if inf in INFO_LIST[1:5]:
            reduction = 90
            converted_info_dict[inf] = 0
            for i in range(crate_num):
                converted_info_dict[inf] = converted_info_dict[inf] + int(info[inf] * reduction / 100.0)
                if not reduction == 50:
                    reduction -= 10
        elif not isinstance(info[inf], int):
            converted_info_dict[inf] = info[inf] * crate_num
    return converted_info_dict


def convert_time_info(craft_input, crate_num):
    info = get_info(craft_input)
    crate_info = info[INFO_LIST[-1]]
    converted_info = crate_info * crate_num
    return converted_info


def get_base_info(craft_input, crate_num):
    info = get_info(craft_input)
    crate_info = info[INFO_LIST[0]]
    converted_info = crate_info * crate_num
    return converted_info


def get_craft_category(craft_item):
    for category in JSON_DATA:
        if craft_item in JSON_DATA[category]:
            return category


def get_categories():
    return [category for category in JSON_DATA]


def get_crafts(category):
    return [craft for craft in JSON_DATA[category]]


def get_category_icon(category):
    return "{}/Icons_category/{}.png".format(_RESSOURCES_PATH, category)


def get_craft_icon(craft):
    category = get_craft_category(craft)
    return "{}/{}/{}.png".format(_RESSOURCES_PATH, category, craft)


def get_resource_icon(resource):
    return "{}/Ressources/{}".format(_RESSOURCES_PATH, resource)


def get_crate_icon():
    return "{}/Ressources/Crate".format(_RESSOURCES_PATH)


def get_time_icon():
    return "{}/Ressources/Time".format(_RESSOURCES_PATH)
