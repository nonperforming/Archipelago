from os import path
from pathlib import Path

from BaseClasses import Item, ItemClassification, Location
from Utils import parse_yaml

GAME_NAME = "rhythm_doctor"

base_path = path.dirname(__file__)
data_path = path.join(base_path, "data")
items_path = path.join(data_path, "items.yml")
locations_path = path.join(data_path, "locations.yml")
options_path = path.join(data_path, "options.yml")
world_path = path.join(data_path, "world.yml")

class RhythmDoctorLocation(Location):
    game = GAME_NAME

class RhythmDoctorItem(Item):
    game = GAME_NAME

# ?
# class ItemData:
#     item_classification: ItemClassification
#     #code

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

def flatten_items(data: dict[str, dict[str, list] | str, list | str, dict[str, any]]) -> list[dict[str, int, str]]:
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

def flatten_items_filler(data: dict[str, dict[str, list] | str, list | str, dict[str, any]]) -> list[dict[str, int, str]]:
    filler_items: list[dict[str, int, str]] = []
    for filler_type in data["filler"].values():
        for filler in filler_type:
            filler_items.append(filler)

    return filler_items

def flatten_items_filler_traps(data: dict[str, dict[str, list] | str, list | str, dict[str, any]]) -> list[dict[str, int, str]]:
    filler_items: list[dict[str, int, str]] = []
    for filler in data["filler"]["traps"]:
        filler_items.append(filler)

    return filler_items

def flatten_items_filler_powerups(data: dict[str, dict[str, list] | str, list | str, dict[str, any]]) -> list[dict[str, int, str]]:
    filler_items: list[dict[str, int, str]] = []
    for filler in data["filler"]["powerups"]:
        filler_items.append(filler)

    return filler_items

def flatten_items_filler_junk(data: dict[str, dict[str, list] | str, list | str, dict[str, any]]) -> list[dict[str, int, str]]:
    filler_items: list[dict[str, int, str]] = []
    for filler in data["filler"]["junk"]:
        filler_items.append(filler)

    return filler_items

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

def get_classification(classification: str) -> ItemClassification:
    match classification:
        case "progression":
            return ItemClassification.progression
        case "filler":
            return ItemClassification.filler
        case "trap":
            return ItemClassification.trap | ItemClassification.filler
        case "useful":
            return ItemClassification.useful
    raise ValueError(f"Rhythm Doctor: Item classification '{classification}' is not valid")

# TODO: type hint
# TODO: item name to id!!
# TODO: item type (instead of list, any)
items_dictionary: dict[str, dict[str, list] | str, list | str, dict[str, any]] = load_data_file(items_path)
locations_dictionary: dict[str, dict[str, list]] = load_data_file(locations_path)
world_dictionary: dict[str, any] = load_data_file(world_path)

flattened_items = flatten_items(items_dictionary)
flattened_items_filler = flatten_items_filler(items_dictionary)
flattened_items_filler_junk = flatten_items_filler_junk(items_dictionary)
flattened_items_filler_powerups = flatten_items_filler_powerups(items_dictionary)
flattened_items_filler_traps = flatten_items_filler_traps(items_dictionary)
flattened_items_nofiller = [item for item in flattened_items if item not in flattened_items_filler]
flattened_locations = flatten_locations(locations_dictionary)