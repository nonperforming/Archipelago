from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from BaseClasses import Item, Location, LocationProgressType

from .Options import EndGoal

if TYPE_CHECKING:
    from . import RhythmDoctorWorld


@dataclass
class _Item:
    name: str
    id: int | None

    def get_item(self) -> tuple[str, int] | None:
        if self.id is None:
            return None

        return self.name, self.id


GAME = "Rhythm Doctor"
REGIONS = ["Main Ward", "SVT Ward", "Train", "Physiotherapy Ward", "Records Room", "Basement", "Garden Room"]
LEVEL_COUNT_IN_ACT = {  # TODO: client should get this information also
    "Act 1": 4,
    "Act 2": 8,
    "Act 3": 6,
    "Act 4": 8,
    "Act 5": 6,
    "Act 6": 2,
    "Act 7": 2,
}

KEYS = [
    _Item("SVT Ward Key", 44),
    _Item("Train Key", 45),
    _Item("Physiotherapy Ward Key", 46),
    _Item("Basement Key", 47),
    _Item("Garden Room Key", 48),
    _Item("Records Room Key", 60),
]

# TODO: Fix ids
FILLER_JUNK = [
    _Item("Sleeve Paint", 49),
]
FILLER_POWERUPS = [
    _Item("Strong Heart Powerup", 50),
    _Item("Easy Difficulty Powerup", 51),
    _Item("Ice Speed Powerup", 52),
]
FILLER_TRAPS = [
    _Item("Fragile Heart Trap", 53),
    _Item("Hard Difficulty Trap", 54),
    _Item("Scramble Characters Trap", 55),
    _Item("Scramble Beatsound Trap", 56),
    _Item("Scramble Hitsound Trap", 57),
    _Item("Chilli Speed Trap", 58),
    _Item("Ghost Tap Trap", 59),
]
FILLER = FILLER_JUNK + FILLER_POWERUPS + FILLER_TRAPS


# region Data
class RhythmDoctorItem(Item):
    game = GAME


class RhythmDoctorLocation(Location):
    game = GAME


# region Stages
@dataclass
class _Stage(_Item, ABC):
    short_name: str
    region_name: Literal[
        "Main Ward", "SVT Ward", "Train", "Physiotherapy Ward", "Records Room", "Basement", "Garden Room"
    ]

    act: Literal["Act 1", "Act 2", "Act 3", "Act 4", "Act 5", "Act 6", "Act 7"] | None
    excluded: bool

    @abstractmethod
    def get_locations(self) -> dict[str, int]:
        raise NotImplementedError


@dataclass
class _RegularStage(_Stage):
    b_rank_location_id: int | None = None
    a_rank_location_id: int | None = None
    s_rank_location_id: int | None = None

    def get_locations(self) -> dict[str, int]:
        locations = {}
        if self.b_rank_location_id is not None:
            name = f"{self.name} - B Rank"
            locations[name] = self.b_rank_location_id
        if self.a_rank_location_id is not None:
            name = f"{self.name} - A Rank"
            locations[name] = self.a_rank_location_id
        if self.s_rank_location_id is not None:
            name = f"{self.name} - S Rank"
            locations[name] = self.s_rank_location_id

        return locations


@dataclass
class _BossStage(_Stage):
    clear_location_id: int | None
    clear_plus_location_id: int | None
    clear_perfect_location_id: int | None

    def get_locations(self) -> dict[str, int]:
        locations = {}
        if self.clear_location_id is not None:
            name = f"{self.name} - Clear"
            locations[name] = self.clear_location_id
        if self.clear_plus_location_id is not None:
            name = f"{self.name} - Complete+ Without Checkpoints"
            locations[name] = self.clear_plus_location_id
        if self.clear_perfect_location_id is not None:
            name = f"{self.name} - Perfect Clear"
            locations[name] = self.clear_perfect_location_id
        return locations


@dataclass
class _RhythmWeightlifterStage(_Stage):
    stages: list[int]

    def get_locations(self) -> dict[str, int]:
        locations = {}
        for stage_number, location_id in enumerate(self.stages, 1):
            name = f"{self.name} - Stage {stage_number} Clear"
            locations[name] = location_id

        return locations


# region Main stages
# fmt: off
main_ward_stages = [
    _RegularStage("1-1 - Samurai Techno", 1, "1-1", "Main Ward", "Act 1", False, 1, 2, 3),
    _RegularStage("1-1N - Samurai Dubstep", 2, "1-1N", "Main Ward", "Act 1", False, 4, 5, 6),
    _RegularStage("1-2 - Intimate", 3, "1-2", "Main Ward", "Act 1", False, 7, 8, 9),
    _RegularStage("1-2N - Intimate (Night)", 4, "1-2N", "Main Ward", "Act 1", False, 10, 11, 12),
    _RegularStage("1-CNY - Chinese New Year", 5, "1-CNY", "Main Ward", "Act 1", False, 13, 14, 15),
    _RegularStage("1-BOO - theme of really spooky bird", 6, "1-BOO", "Main Ward", "Act 1", False, 16, 17, 18),
    _RegularStage("3-1 - Sleepy Garden", 7, "3-1", "Main Ward", "Act 3", False, 21, 22, 23),
    _RegularStage("3-1N - Lounge", 8, "3-1N", "Main Ward", "Act 3", False, 24, 25, 26),
    _RegularStage("3-2 - Classy", 9, "3-2", "Main Ward", "Act 3", False, 27, 28, 29),
    _RegularStage("3-2N - Classy (Night)", 10, "3-2N", "Main Ward", "Act 3", False, 30, 31, 32),
    _RegularStage("3-3 - Distant Duet", 11, "3-3", "Main Ward", "Act 3", False, 33, 34, 35),
    _RegularStage("3-3N - Distant Duet (Night)", 12, "3-3N", "Main Ward", "Act 3", False, 36, 37, 38),
]

svt_ward_stages = [
    _RegularStage("2-1 - Lo-fi Hip-Hop Beats To Treat Patients To", 13, "2-1", "SVT Ward", "Act 2", False, 43, 44, 45),
    _RegularStage("2-1N - wish i could care less", 14, "2-1N", "SVT Ward", "Act 2", False, 46, 47, 48),
    _RegularStage("2-2 - Supraventricular Tachycardia", 15, "2-2", "SVT Ward", "Act 2", False, 49, 50, 51),
    _RegularStage("2-2N - Unreachable", 16, "2-2N", "SVT Ward", "Act 2", False, 52, 53, 54),
    _RegularStage("2-3 - Puff Piece", 17, "2-3", "SVT Ward", "Act 2", False, 55, 56, 57),
    _RegularStage("2-3N - Bomb-Sniffing Pomeranian", 18, "2-3N", "SVT Ward", "Act 2", False, 58, 59, 60),
    _RegularStage("2-4 - Song of the Sea", 19, "2-4", "SVT Ward", "Act 2", True, s_rank_location_id=61),
    _RegularStage("2-4N - Song of the Sea (Night)", 20, "2-4N", "SVT Ward", "Act 2", True, s_rank_location_id=62),
    _RegularStage("2-B1 - Beans Hopper", 21, "2-B1", "SVT Ward", "Act 2", False, 63, 64, 65),
    _BossStage("2-XN - Bitter Times", 60, "2-XN", "SVT Ward", "Act 7", False, 150, 151, 152)
]

train_stages = [
    _RegularStage("4-1 - Training Doctor's Train Ride Performance", 22, "4-1", "Train", "Act 4", False, 68, 69, 70),
    _RegularStage("4-1N - Rollerdisco Rumble", 23, "4-1N", "Train", "Act 4", False, 71, 72, 73),
    _RegularStage("4-2 - Invisible", 24, "4-2", "Train", "Act 4", False, 74, 75, 76),
    _RegularStage("4-2N - Invisible (Night)", 25, "4-2N", "Train", "Act 4", False, 77, 78, 79),
    _RegularStage("4-3 - Steinway", 26, "4-3", "Train", "Act 4", False, 80, 81, 82),
    _RegularStage("4-3N - Steinway Reprise", 27, "4-3N", "Train", "Act 4", False, 83, 84, 85),
    _RegularStage("4-4 - Know You", 28, "4-4", "Train", "Act 4", False, 86, 87, 88),
    _RegularStage("4-4N - Murmurs", 29, "4-4N", "Train", "Act 4", False, 89, 90, 91),
]

physiotherapy_ward_stages = [
    _RegularStage("5-1 - Lucky Break", 30, "5-1", "Physiotherapy Ward", "Act 5", False, 94, 95, 96),
    _RegularStage("5-1N - One Slip Too Late", 31, "5-1N", "Physiotherapy Ward", "Act 5", False, 97, 98, 99),
    _RegularStage("5-2 - Lo-fi Beats For Patients To Chill To", 32, "5-2", "Physiotherapy Ward", "Act 5", False, 100, 101, 102),
    _RegularStage("5-2N - Unsustainable Inconsolable", 33, "5-2N", "Physiotherapy Ward", "Act 5", False, 103, 104, 105),
    _RegularStage("5-3 - Seventh-Inning Stretch", 34, "5-3", "Physiotherapy Ward", "Act 5", True, s_rank_location_id=106),
    _RegularStage("5-3N - Corazones Viejos", 61, "5-3N", "Physiotherapy Ward", "Act 5", False, 147, 148, 149),
    _RhythmWeightlifterStage(
        "5-B1 - Rhythm Weightlifter",
        44,
        "5-B1",
        "Physiotherapy Ward",
        "Act 5",
        False,
        stages=[107, 108, 109, 110, 111, 112, 113, 114, 115, 116],
    ),
]

record_room_stages = [
    _RegularStage("6-1 - Something To Tell You", 62, "6-1", "Records Room", "Act 6", False, 153, 154, 155),
    _RegularStage("6-2 - Welcome Back", 63, "6-2", "Records Room", "Act 6", False, 156, 157, 158),
    _RegularStage("7-1 - Blurred", 64, "7-1", "Records Room", "Act 7", False, 159, 160, 161),
]

other_stages = [
    _RegularStage("X-FTS - Fixations Towards the Stars", 35, "X-FTS", "Basement", None, False, 120, 121, 122),
    _RegularStage("X-KOB - Kingdom of Balloons", 36, "X-KOB", "Basement", None, False, 123, 124, 125),
    _RegularStage("X-WOT - Worn Out Tapes", 37, "X-WOT", "Basement", None, False, 126, 127, 128),
    _RegularStage("X-MAT - Meet and Tweet", 38, "X-MAT", "Basement", None, False, 129, 130, 131),
    _RegularStage("MD-1 - Blackest Luxury Car", 39, "MD-1", "Basement", None, False, 132, 133, 134),
    _RegularStage("MD-2 - tape/stop/night", 40, "MD-2", "Basement", None, False, 135, 136, 137),
    _RegularStage("MD-3 - The 90's Decision", 41, "MD-3", "Basement", None, False, 138, 139, 140),
    _RegularStage("X-0 - Helping Hands", 42, "X-0", "Garden Room", None, False, 141, 142, 143),
    _RegularStage("X-1 - Art Exercise", 43, "X-1", "Basement", None, False, 144, 145, 146),
]
"""
Stages that don't have a corresponding boss song or act.
"""
# fmt: on

all_regular_stages = (
    main_ward_stages + svt_ward_stages + train_stages + physiotherapy_ward_stages + record_room_stages + other_stages
)
# endregion

# region Bosses
act_1_boss = _BossStage("1-X - Battleworn Insomniac", None, "1-X", "Main Ward", "Act 1", False, 19, None, 20)
act_2_boss = _BossStage("2-X - All The Times", None, "2-X", "SVT Ward", "Act 2", False, 66, None, 67)
act_3_boss = _BossStage("3-X - One Shift More", None, "3-X", "Main Ward", "Act 3", False, 39, None, 40)
act_3_secret_boss = _BossStage("3-DOG - Rhythm Dogtor", None, "3-DOG", "Main Ward", "Act 3", False, 41, None, 42)
act_4_boss = _BossStage("4-X - Super Battleworn Insomniac", None, "1-XN", "Main Ward", "Act 4", False, 92, None, 93)
act_5_boss = _BossStage("5-X - Dreams Don't Stop", None, "5-X", "Physiotherapy Ward", "Act 5", False, 117, 118, 119)
act_6_boss = _BossStage("6-X - Boss Fight", None, "6-X", "Records Room", "Act 6", False, 162, 163, 164)
act_7_bosses = [  # For the sake of logic, the Abandoned Ward does not require a key, and is considered to be a part of the Main Ward.
    _BossStage("7-X - Miracle Defibrillator", None, "7-X", "Main Ward", "Act 7", False, 165, 166, 167),
    _BossStage("7-X2 - Miracle Defibrillator (Cole's Song)", None, "7-X2", "Main Ward", "Act 7", False, 168, 169, 170),
]

all_boss_stages: list[_BossStage] = [
    act_1_boss,
    act_2_boss,
    act_3_boss,
    act_3_secret_boss,
    act_4_boss,
    act_5_boss,
    act_6_boss,
    *act_7_bosses,
]

# endregion

all_stages = all_regular_stages + all_boss_stages
# endregion

# endregion

all_items = all_regular_stages + FILLER + KEYS
# endregion


@dataclass
class _Stage(ABC):
    name: str
    excluded: bool

    @abstractmethod
    def get_locations(self) -> dict[str, int]:
        raise NotImplementedError


def create_items(world: "RhythmDoctorWorld"):
    # Get a random level in the Main Ward to start with
    # At runtime this seems to be a frozenset, not a list (for some reason???)
    start_with_item = world.random.choice(list(world.item_name_groups["Act 1"] | world.item_name_groups["Act 3"]))

    def create_item(item: _Item) -> None:
        rd_item = world.create_item(item.name)
        if item.name == start_with_item:
            world.push_precollected(rd_item)
        else:
            item_pool.append(rd_item)

    def pad_with_filler() -> None:
        for _ in range(total_locations - len(item_pool)):
            item_pool.append(world.create_filler())

    total_locations = len(world.multiworld.get_unfilled_locations(world.player))
    item_pool = []

    for item in all_items:
        if (
            world.options.end_goal.value == EndGoal.option_helping_hands
            and isinstance(item, _RegularStage)
            and item.short_name == "X-0"
        ):
            continue

        create_item(item)
    pad_with_filler()

    world.multiworld.itempool += item_pool


def create_locations(world: "RhythmDoctorWorld"):
    def create_locations_from_stage(stage: _Stage):
        # TODO: Could probably do with a clean up
        locations = stage.get_locations()
        world.get_region(stage.short_name).add_locations(locations, RhythmDoctorLocation)

        if stage.excluded:
            for location_name in locations.keys():
                world.get_location(location_name).progress_type = LocationProgressType.EXCLUDED
        elif stage.short_name == "5-B1":
            for stage_number in range(5, 11):
                world.get_location(
                    f"5-B1 - Rhythm Weightlifter - Stage {stage_number} Clear"
                ).progress_type = LocationProgressType.EXCLUDED
        else:
            if isinstance(stage, _BossStage):
                for location_name in locations.keys():
                    world.get_location(location_name).progress_type = LocationProgressType.PRIORITY

            if world.options.perfect_ranks_excluded.value:
                if isinstance(stage, _RegularStage) and stage.s_rank_location_id is not None:
                    world.get_location(f"{stage.name} - S Rank").progress_type = LocationProgressType.EXCLUDED
                elif isinstance(stage, _BossStage) and stage.clear_perfect_location_id is not None:
                    world.get_location(f"{stage.name} - Perfect Clear").progress_type = LocationProgressType.EXCLUDED

    for stage in all_stages:
        if stage.short_name == "X-0" and world.options.end_goal.value == EndGoal.option_helping_hands:
            continue

        create_locations_from_stage(stage)


def get_location_name_to_id() -> dict[str, int]:
    location_name_to_id = {}

    for stage in all_stages:
        for location_name, location_id in stage.get_locations().items():
            location_name_to_id[location_name] = location_id

    return location_name_to_id


def get_item_name_to_id() -> dict[str, int]:
    item_name_to_id = {}

    for item_name, item_id in [item.get_item() for item in all_items if item.get_item() is not None]:
        item_name_to_id[item_name] = item_id

    return item_name_to_id
