#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author
"""

import os
import datetime
import json

_SCRIPT_PATH = os.path.abspath(__file__)
_DIR_PATH = os.path.dirname(_SCRIPT_PATH)
_JSON_PATH = "{}/data.json".format(_DIR_PATH)

INFO_LIST = ["Unit par crate", "B. Mat", "E. Mat", "H.E. MAt", "R. Mat", "Time (seconds)"]


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


def convert_info(craft_input, crate_num):
    info = get_info(craft_input)
    converted_info_dict = {}
    for idx, inf in enumerate(info):
        if inf in INFO_LIST[1:5]:
            reduction = 90
            converted_info_dict[inf] = 0
            for i in range(crate_num):
                converted_info_dict[inf] = converted_info_dict[inf] + int(info[inf] * reduction / 100.0)
                if not reduction == 50:
                    reduction -= 10
        elif not info[inf] == '?':
            converted_info_dict[inf] = info[inf] * crate_num
    if not info[INFO_LIST[-1]] == '?':
        now = datetime.datetime.now()
        converted_date_time = datetime.timedelta(seconds=converted_info_dict[INFO_LIST[-1]])
        delivery_time = now + converted_date_time
        converted_info_dict['Delivery date'] = delivery_time.strftime("%d/%m/%Y %H:%M:%S")
    return converted_info_dict


def create_info_text(craft_input, crate_num):
    info = convert_info(craft_input, crate_num)
    text = '{}\nFor {} crates.\n==========\n'.format(craft_input, crate_num)
    for inf in info:
        if inf == INFO_LIST[0]:
            text += 'Total unite crafted: {}\n'.format(info[inf])
        else:
            if not info[inf] == 0:
                text += '{}: {}\n'.format(inf, info[inf])
    return text


def get_craft_category(craft_item):
    for category in JSON_DATA:
        if craft_item in JSON_DATA[category]:
            return category


def get_categories():
    return [category for category in JSON_DATA]


def get_crafts(category):
    return [craft for craft in JSON_DATA[category]]
