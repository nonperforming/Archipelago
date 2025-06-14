import random

from BaseClasses import Tutorial
from worlds.AutoWorld import World, WebWorld
from typing import List, Dict, Mapping, Any
from .Data import items_dictionary, locations_dictionary, world_dictionary, flattened_items, flattened_locations
from .Options import RhythmDoctorOptions

# Get multiworld data
items = items_dictionary
locations = locations_dictionary
world = world_dictionary

class RhythmDoctorWeb(WebWorld):
    rich_text_options_doc = True
    theme = "partyTime"
    bug_report_page = "https://github.com/nonperforming/RhythmDoctor.Archipelago/issues"

    # TODO: Where to put game page?
    # Other worlds only have setup here
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide for setting up Rhythm Doctor for Archipelago.",
        "English",
        "setup_en_US.md",
        "setup/en", # setup/en or setup/en_US?
        [""] # TODO: Fill this in with whoever writes the doc
    )]

    options_presets = Options.presets
    option_groups = Options.groups

class RhythmDoctorWorld(World):
    """
    Save lives with your spacebar!

    Rhythm Doctor is a rhythm game in a world where defibrillating patients' hearts in sync with their heartbeats has healing properties.
    Slam your spacebar in perfect time on the 7th beat, and they might just come out okay.

    In Archipelago, levels and wards are randomized. Clearing levels with B, A, and S ranks will clear locations.
    Boss levels unlock after a certain amount of levels in its act has been cleared.
    """ # Excerpt from Steam store page

    game = "Rhythm Doctor"
    web = RhythmDoctorWeb()
    #required_client_version = (world["version"], 0, 0)
    required_client_version = (0, 5, 0)

    options_dataclass: RhythmDoctorOptions
    options: RhythmDoctorOptions
    #settings_key = "rhythm_doctor_settings"
    #settings: ClassVar[RhythmDoctorSettings]

    origin_region_name = "Main Ward"
    topology_present = True # TODO: I think this should be on. Check if the paths are valid!!

    # items.yml has items classified by levels, keys, filler (powerups, traps, junk) etc.
    # We need to "flatten" it here as item_name_to_id wants type Dict[str, int]
    # TODO: Do we need this?
    #@staticmethod
    #def is_item(item: Any | Dict) -> bool:
    #    return "name" in item and "id" in item and "classification" in item

    item_name_to_id = {item["name"]: item["id"] for item in flattened_items}
    location_name_to_id = {location["name"]: location["id"] for location in flattened_locations}

    # TODO: Items other than levels probably don't need to be here, is there any other use for them here?
    # Is leaving them here safe?
    item_name_groups = {
        # FIXME: invalid syntax
        "Act 1 Levels": [level["name"] for level in items_dictionary["levels"]["main-ward"] if level["name"].startswith("1-")],
        "Act 2 Levels": [level["name"] for level in items_dictionary["levels"]["svt-ward"]],
        "Act 3 Levels": [level["name"] for level in items_dictionary["levels"]["main-ward"] if level["name"].startswith("3-")],
        "Act 4 Levels": [level["name"] for level in items_dictionary["levels"]["train"]],
        "Act 5 Levels": [level["name"] for level in items_dictionary["levels"]["physiotherapy-ward"]],
        "Keys": [item["name"] for item in items_dictionary["keys"]],
        "Junk": [item["name"] for item in items_dictionary["filler"]["junk"]],
        "Powerups": [item["name"] for item in items_dictionary["filler"]["powerups"]],
        "Traps": [item["name"] for item in items_dictionary["filler"]["traps"]],
    }

    def generate_early(self) -> None:
        # TODO: Does this work?
        # TODO: Should create_item be called here?
        #       self.multiworld.push_precollected(self.create_item(self.random.choice(items_dictionary["levels"]["main-ward"])))
        #self.multiworld.push_precollected(self.create_item(self.random.choice(items_dictionary["levels"]["main-ward"])))
        # TODO: implement
        pass

    def create_regions(self) -> None:
        from .Regions import create_regions
        create_regions(self.multiworld, self.player)

    """
    def fill_slot_data(self) -> Mapping[str, Any]:
        # TODO: How does this work? How is this meant to work?

        return self.options.as_dict(
            "end_goal",
            "boss_unlock_requirement",
            "trap_chance",
            "enable_fragile_heart_trap",
            "enable_character_scramble_trap",
            "enable_beatsound_scramble_trap",
            "enable_hitsound_scramble_trap",
            "enable_hard_difficulty_trap",
            "enable_speed_trap",
            "enable_easy_difficulty_powerup",
            "enable_strong_heart_powerup",
            "enable_slow_powerup",
            "death_link",
        )
    """

    def set_rules(self) -> None:
        from .Rules import set_rules
        set_rules(self)

