from collections.abc import Mapping
from typing import Any

from BaseClasses import ItemClassification

from Options import OptionError
from worlds.AutoWorld import World

from .Data import (
    FILLER_JUNK,
    FILLER_POWERUPS,
    FILLER_TRAPS,
    GAME,
    RhythmDoctorItem,
    all_boss_stages,
    all_stages,
    create_items,
    create_locations,
    get_item_name_to_id,
    get_location_name_to_id,
)
from .Options import RhythmDoctorOptions
from .Regions import create_and_connect_regions
from .Rules import set_rules
from .Web import RhythmDoctorWeb


class RhythmDoctorWorld(World):
    """
    Save lives with your spacebar!

    Rhythm Doctor is a rhythm game in a world where defibrillating patients' hearts in sync with their heartbeats has healing properties.
    Slam your spacebar in perfect time on the 7th beat, and they might just come out okay.

    In Archipelago, levels and access to wards are randomized. Clearing levels with B, A, and S ranks will clear locations.
    Boss levels unlock after a certain amount of levels in its act has been cleared.
    """  # Excerpt from Steam store page

    game = GAME
    web = RhythmDoctorWeb()

    options_dataclass = RhythmDoctorOptions
    options: RhythmDoctorOptions

    origin_region_name = "Main Ward"
    topology_present = True  # TODO: Check if this is correct

    location_name_to_id = get_location_name_to_id()
    item_name_to_id = get_item_name_to_id()

    # Populate item_name_groups
    # FIXME: frozenset or list?
    local_item_name_groups: dict[str, list[str]] = {"Stages": []}
    for stage in all_stages:
        if stage.act is None:
            continue
        if stage in all_boss_stages:
            continue

        if stage.act not in local_item_name_groups:
            local_item_name_groups[stage.act] = []
        local_item_name_groups[stage.act].append(stage.name)
        local_item_name_groups["Stages"].append(stage.name)
    local_item_name_groups["Junk"] = []
    for junk in FILLER_JUNK:
        local_item_name_groups["Junk"].append(junk)
    local_item_name_groups["Powerups"] = []
    for powerup in FILLER_POWERUPS:
        local_item_name_groups["Powerups"].append(powerup)
    local_item_name_groups["Traps"] = []
    for trap in FILLER_TRAPS:
        local_item_name_groups["Traps"].append(trap)
    item_name_groups = local_item_name_groups

    def create_regions(self) -> None:
        create_and_connect_regions(self)
        create_locations(self)

    def set_rules(self) -> None:
        set_rules(self)

        from .tools import GenerateClientData

        GenerateClientData.main(self)

    def create_items(self) -> None:
        create_items(self)

    def create_item(self, name: str) -> RhythmDoctorItem:
        def get_classification() -> ItemClassification:
            # TODO: Get real item classification
            return ItemClassification.progression

        return RhythmDoctorItem(name, get_classification(), self.item_name_to_id[name], self.player)

    def create_filler(self) -> RhythmDoctorItem:
        # TODO: Currently ignores user input on trap preferences
        #       i.e. self.options.enable_chilli_speed_trap
        # Check which filler type to get
        result = self.random.randrange(100)

        trap_pool = list(self.item_name_groups["Traps"])
        if not self.options.enable_fragile_heart_traps.value:
            trap_pool.remove("Fragile Heart Trap")
        if not self.options.enable_character_scramble_traps.value:
            trap_pool.remove("Scramble Characters Trap")
        if not self.options.enable_beatsound_scramble_traps.value:
            trap_pool.remove("Scramble Beatsound Trap")
        if not self.options.enable_hitsound_scramble_traps.value:
            trap_pool.remove("Scramble Hitsound Trap")
        if not self.options.enable_hard_difficulty_traps.value:
            trap_pool.remove("Hard Difficulty Trap")
        if not self.options.enable_chilli_speed_traps.value:
            trap_pool.remove("Chilli Speed Trap")
        if not self.options.enable_ghost_tap_traps.value:
            trap_pool.remove("Ghost Tap Trap")

        powerup_pool = list(self.item_name_groups["Powerups"])
        if not self.options.enable_easy_difficulty_powerups.value:
            powerup_pool.remove("Easy Difficulty Powerup")
        if not self.options.enable_strong_heart_powerups.value:
            powerup_pool.remove("Strong Heart Powerup")
        if not self.options.enable_ice_speed_powerups.value:
            powerup_pool.remove("Ice Speed Powerup")

        classification = ItemClassification.filler
        if result < self.options.trap_chance.value:
            pool = trap_pool
            classification = ItemClassification.trap
        elif result < self.options.trap_chance.value + self.options.powerup_chance.value:
            pool = powerup_pool
        else:
            # FIXME: Currently Sleeve Paint is not progressive - so it should only have one item.
            pool = self.item_name_groups["Junk"]

        item_name = self.random.choice(list(pool))
        item = self.create_item(item_name)
        item.classification = classification
        return item

    def get_filler_item_name(self) -> str:
        return "A Bit of Rhythm"

    def generate_early(self) -> None:
        if (self.options.trap_chance.value + self.options.powerup_chance.value) > 100:
            raise OptionError(
                f"Rhythm Doctor: Player {self.player_name}'s set",
                f"trap chance ({self.options.trap_chance}) and"
                f"powerup chance ({self.options.powerup_chance}) are over 100%",
            )
        if self.options.trap_chance.value != 0 and not (
            self.options.enable_fragile_heart_traps.value
            or self.options.enable_character_scramble_traps.value
            or self.options.enable_beatsound_scramble_traps.value
            or self.options.enable_hitsound_scramble_traps.value
            or self.options.enable_hard_difficulty_traps.value
            or self.options.enable_chilli_speed_traps.value
        ):
            raise OptionError(
                f"Rhythm Doctor: Player {self.player_name}'s set trap chance "
                f"is {self.options.trap_chance}, but all traps are disabled"
            )
        if self.options.powerup_chance.value != 0 and not (
            self.options.enable_easy_difficulty_powerups.value
            or self.options.enable_strong_heart_powerups.value
            or self.options.enable_ice_speed_powerups.value
        ):
            raise OptionError(
                f"Rhythm Doctor: Player {self.player_name}'s set powerup chance "
                f"is {self.options.trap_chance}, but all powerups are disabled"
            )

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
            "end_goal",
            "boss_unlock_requirement",
            "death_link",
        )
