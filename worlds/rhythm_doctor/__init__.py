from typing import Mapping, Any, TYPE_CHECKING

from BaseClasses import ItemClassification
from worlds.AutoWorld import World

from .Data import GAME, RhythmDoctorItem, create_items, get_location_name_to_id, get_item_name_to_id, create_locations, all_stages
from .Regions import create_and_connect_regions
from .Web import RhythmDoctorWeb


class RhythmDoctorWorld(World):
    """
    Save lives with your spacebar!

    Rhythm Doctor is a rhythm game in a world where defibrillating patients' hearts in sync with their heartbeats has healing properties.
    Slam your spacebar in perfect time on the 7th beat, and they might just come out okay.

    In Archipelago, levels and wards are randomized. Clearing levels with B, A, and S ranks will clear locations.
    Boss levels unlock after a certain amount of levels in its act has been cleared.
    """  # Excerpt from Steam store page

    game = GAME
    web = RhythmDoctorWeb()

    origin_region_name = "Main Ward"
    topology_present = True  # TODO: Check if this is correct

    location_name_to_id = get_location_name_to_id()
    item_name_to_id = get_item_name_to_id()

    # Populate item_name_groups
    item_name_groups: dict[str, list[str]] = {}
    for stage in all_stages:
        if stage.act is None:
            continue

        if stage.act not in item_name_groups:
            item_name_groups[stage.act] = []
        item_name_groups[stage.act].append(stage.name)

    # item_name_groups = {
    #
    #     # "Act 1 Levels": [level["name"] for level in data.items_dictionary["levels"]["main-ward"] if
    #     #                  level["name"].startswith("1-") and not level["name"] == "1-XN"],
    #     # "Act 2 Levels": [level["name"] for level in data.items_dictionary["levels"]["svt-ward"]],
    #     # "Act 3 Levels": [level["name"] for level in data.items_dictionary["levels"]["main-ward"] if
    #     #                  level["name"].startswith("3-")],
    #     # "Act 4 Levels": [level["name"] for level in data.items_dictionary["levels"]["train"]] +
    #     #                 [level["name"] for level in data.items_dictionary["levels"]["main-ward"] if
    #     #                  level["name"].startswith("1-XN")],
    #     # "Act 5 Levels": [level["name"] for level in data.items_dictionary["levels"]["physiotherapy-ward"]],
    #     # "Keys": [item["name"] for item in data.items_dictionary["keys"]],
    #     # "Junk": [item["name"] for item in data.items_dictionary["filler"]["junk"]],
    #     # "Powerups": [item["name"] for item in data.items_dictionary["filler"]["powerups"]],
    #     # "Traps": [item["name"] for item in data.items_dictionary["filler"]["traps"]],
    # }

    def create_regions(self) -> None:
        create_and_connect_regions(self)
        create_locations(self)

    def set_rules(self) -> None:
        # TODO
        pass

    def create_items(self) -> None:
        create_items(self)

    def create_item(self, name: str) -> RhythmDoctorItem:
        def get_classification() -> ItemClassification:
            # TODO: Get real item classification
            return ItemClassification.progression

        return RhythmDoctorItem(name, get_classification(), self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        return "A Bit of Rhythm"

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
            "end_goal",
            "boss_unlock_requirement",
            "death_link",
        )
