from typing import ClassVar

from BaseClasses import Tutorial, Item, ItemClassification, Location
from Options import OptionError
from worlds.AutoWorld import World, WebWorld
from .Data import items_dictionary, locations_dictionary, world_dictionary, \
    flattened_items, flattened_items_filler, flattened_items_filler_junk, flattened_items_filler_powerups, \
    flattened_items_filler_traps, flattened_items_nofiller, \
    flattened_locations, \
    get_classification

from .Options import RhythmDoctorOptions

GAME = "Rhythm Doctor"

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
        "setup/en_US",
        [""]  # TODO: Fill this in with whoever writes the doc
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
    """  # Excerpt from Steam store page

    game = GAME
    web = RhythmDoctorWeb()
    required_client_version = (0, 5, 0)

    options_dataclass = RhythmDoctorOptions
    options: RhythmDoctorOptions

    origin_region_name = "Main Ward"
    topology_present = True  # TODO: I think this should be on. Check if the paths are valid!!

    # items.yml has items classified by levels, keys, filler (powerups, traps, junk) etc.
    # We need to "flatten" it here as item_name_to_id wants type Dict[str, int]
    # TODO: Do we need this?
    # @staticmethod
    # def is_item(item: Any | Dict) -> bool:
    #    return "name" in item and "id" in item and "classification" in item

    item_name_to_id = {item["name"]: item["id"] for item in flattened_items}
    location_name_to_id = {location["name"]: location["id"] for location in flattened_locations}

    # TODO: Items other than levels probably don't need to be here, is there any other use for them here?
    # Is leaving them here safe?
    item_name_groups = {
        # FIXME: invalid syntax
        "Act 1 Levels": [level["name"] for level in items_dictionary["levels"]["main-ward"] if
                         level["name"].startswith("1-")],
        "Act 2 Levels": [level["name"] for level in items_dictionary["levels"]["svt-ward"]],
        "Act 3 Levels": [level["name"] for level in items_dictionary["levels"]["main-ward"] if
                         level["name"].startswith("3-")],
        "Act 4 Levels": [level["name"] for level in items_dictionary["levels"]["train"]],
        "Act 5 Levels": [level["name"] for level in items_dictionary["levels"]["physiotherapy-ward"]],
        "Keys": [item["name"] for item in items_dictionary["keys"]],
        "Junk": [item["name"] for item in items_dictionary["filler"]["junk"]],
        "Powerups": [item["name"] for item in items_dictionary["filler"]["powerups"]],
        "Traps": [item["name"] for item in items_dictionary["filler"]["traps"]],
    }

    def generate_early(self) -> None:
        # TODO: Need to finish

        # Check validity of options
        # Check if sum of Trap Chance and Powerup Chance is over 100
        if (self.options.trap_chance + self.options.powerup_chance) > 100:
            # Format taken from Blasphemous
            raise OptionError(f"Rhythm Doctor: Player {self.player_name}'s set",
                              f"trap chance ({self.options.trap_chance}) and"
                              f"powerup chance ({self.options.powerup_chance}) are over 100%")
        # TODO: Check if all traps are disabled but trap chance is not 0

    def create_items(self) -> None:
        # We need to pull a level from the Main Ward and push it into our start inventory.
        starting_level_dict = self.random.choice(items_dictionary["levels"]["main-ward"])
        starting_level = self.create_item(starting_level_dict)
        self.multiworld.push_precollected(starting_level)

        for item_dict in flattened_items_nofiller:
            if item_dict == starting_level_dict:
                # Do not add the level we start with to the pool.
                continue
            item = self.create_item(item_dict)
            item.classification = get_classification(item_dict["classification"])
            self.multiworld.itempool.append(item)

        # Add filler items to pad leftover locations
        for i in range(len(self.multiworld.get_unfilled_locations(self.player))):
            self.multiworld.itempool.append(self.get_filler())

        pass

    def create_item(self, item_dictionary: dict[str, str | int]) -> Data.RhythmDoctorItem:
        # Is it safe to have name be an item dict
        # '{'name': '1-1 - Samurai Techno', 'id': 8210412168114000, 'classification': 'progression'}'?

        # item = flattened_items[self.item_name_to_id[name] - 82_104_121_68_114_000]
        # id = item["id"]
        # classification = self.get_classification(item["classification"])
        # return Data.RhythmDoctorItem(name, classification, id, self.player)

        return Data.RhythmDoctorItem(item_dictionary["name"],
                                     get_classification(item_dictionary["classification"]),
                                     item_dictionary["id"],
                                     self.player)

    def get_filler(self) -> Data.RhythmDoctorItem:
        # TODO: Currently ignores user input on trap preferences
        #       i.e. self.options.enable_chilli_speed_trap
        # Check which filler type to get
        result = self.random.randint(0, 199)

        classification = ItemClassification.filler
        if result < self.options.trap_chance:
            filler_items = flattened_items_filler_junk
            classification = ItemClassification.trap
        elif result < self.options.trap_chance + self.options.powerup_chance:
            filler_items = flattened_items_filler_traps
        else:
            filler_items = flattened_items_filler_junk

        item_dict = self.random.choice(filler_items)
        item = self.create_item(item_dict)
        item.classification = classification
        return self.create_item(item_dict)

    # def get_filler_item_name(self) -> str:
    #    # Check which filler type to get
    #    result = self.random.randint(0, 199)
    #
    #    if result < self.options.trap_chance:
    #        filler_items = flattened_items_filler_junk
    #    elif result < self.options.trap_chance + self.options.powerup_chance:
    #        filler_items = flattened_items_filler_traps
    #    else:
    #        filler_items = flattened_items_filler_junk
    #
    #    return self.random.choice([item_name["name"] for item_name in filler_items])

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
