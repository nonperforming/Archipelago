from os import path
from pathlib import Path

from BaseClasses import Item, ItemClassification
from Utils import parse_yaml

GAME_NAME = "Rhythm Doctor"

base_path = path.dirname(__file__)
data_path = path.join(base_path, "data")
items_path = path.join(data_path, "items.yml")
locations_path = path.join(data_path, "locations.yml")
options_path = path.join(data_path, "options.yml")
world_path = path.join(data_path, "world.yml")

class RhythmDoctorItem(Item):
    game: str = GAME_NAME

class ItemData:
    item_classification: ItemClassification
    #code

def load_data_file(file_path: str)\
    -> (dict[str, dict[str, list] | str, list | str, dict[str, any]]
        | dict[str, dict[str, list]]
        | dict[str, any]):
    """
    TODO: docstring
    """
    return parse_yaml(Path(file_path).read_text())

def convert_items(data: dict) -> dict[str, ItemClassification]:
    pass
    # TODO???

def flatten_items(data: dict[str, dict[str, list] | str, list | str, dict[str, any]]) -> list:
    """
    TODO
    """
    flattened_items: list = []

    # TODO: Use list comprehension
    # Flattening levels: dict[str, list] (ward name, list of items)
    for ward in data["levels"].values():
        for level in ward:
            flattened_items.append(level)

    # Flattening keys: list
    for key in data["keys"]:
        flattened_items.append(key)

    # Flattening filler: dict[str, list]
    for filler_type in data["filler"].values():
        for filler in filler_type:
            flattened_items.append(filler)

    return flattened_items

def flatten_locations(data: dict[str, dict[str, list]]):
    """
    TODO
    """
    flattened_locations: list = []

    for ward in data["locations"].values():
        for levels in ward.values():
            for level in levels:
                flattened_locations.append(level)

    return flattened_locations

# TODO: type hint
# TODO: item name to id!!
# TODO:                                    vvv ------------- vvv ----------------- vvv --> What should item type be?
items_dictionary: dict[str, dict[str, list] | str, list | str, dict[str, any]] = load_data_file(items_path)
locations_dictionary: dict[str, dict[str, list]] = load_data_file(locations_path)
world_dictionary: dict[str, any] = load_data_file(world_path)

flattened_items = flatten_items(items_dictionary)
flattened_locations = flatten_locations(locations_dictionary)