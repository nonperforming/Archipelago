from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from BaseClasses import Item, Location, LocationProgressType

from .Options import EndGoal

if TYPE_CHECKING:
    from . import RhythmDoctorWorld

GAME = "Rhythm Doctor"
REGIONS = ["Main Ward", "SVT Ward", "Train", "Physiotherapy Ward", "Basement", "Art Room"]

FILLER_JUNK = ["Sleeve Paint"]
FILLER_POWERUPS = ["Strong Heart Powerup", "Easy Difficulty Powerup", "Ice Speed Powerup"]
FILLER_TRAPS = [
    "Fragile Heart Trap",
    "Hard Difficulty Trap",
    "Scramble Characters Trap",
    "Scramble Beatsound Trap",
    "Scramble Hitsound Trap",
    "Chilli Speed Trap",
    "Ghost Tap Trap",
]
FILLER = FILLER_JUNK + FILLER_POWERUPS + FILLER_TRAPS


# region Data
class RhythmDoctorItem(Item):
    game = GAME


class RhythmDoctorLocation(Location):
    game = GAME


@dataclass
class _Stage(ABC):
    name: str
    short_name: str
    region_name: Literal["Main Ward", "SVT Ward", "Train", "Physiotherapy Ward", "Basement", "Art Room"]
    act: Literal["Act 1", "Act 2", "Act 3", "Act 4", "Act 5"] | None
    excluded: bool = False

    @abstractmethod
    def get_locations(self, world: "RhythmDoctorWorld") -> dict[str, int]:
        pass


@dataclass
class _RegularStage(_Stage):
    b_rank_location: bool = True
    a_rank_location: bool = True
    s_rank_location: bool = True

    def get_locations(self, world: "RhythmDoctorWorld") -> dict[str, int]:
        locations = {}
        if self.b_rank_location:
            name = f"{self.name} - B Rank"
            locations[name] = world.location_name_to_id[name]
        if self.a_rank_location:
            name = f"{self.name} - A Rank"
            locations[name] = world.location_name_to_id[name]
        if self.s_rank_location:
            name = f"{self.name} - S Rank"
            locations[name] = world.location_name_to_id[name]

        return locations


@dataclass
class _BossStage(_Stage):
    clear_location: bool = True
    clear_plus_location: bool = False
    clear_perfect_location: bool = True

    def get_locations(self, world: "RhythmDoctorWorld") -> dict[str, int]:
        locations = {}
        if self.clear_location:
            name = f"{self.name} - Clear"
            locations[name] = world.location_name_to_id[name]
        if self.clear_plus_location:
            name = f"{self.name} - Complete+ Without Checkpoints"
            locations[name] = world.location_name_to_id[name]
        if self.clear_perfect_location:
            name = f"{self.name} - Perfect Clear"
            locations[name] = world.location_name_to_id[name]
        return locations


@dataclass
class _RhythmWeightlifterStage(_Stage):
    def get_locations(self, world: "RhythmDoctorWorld") -> dict[str, int]:
        locations = {}
        for stage_number in range(1, 11):
            name = f"{self.name} - Stage {stage_number} Clear"
            locations[name] = world.location_name_to_id[name]

        return locations

# region Main stages
main_ward_stages = [
    _RegularStage("1-1 - Samurai Techno", "1-1", "Main Ward", "Act 1"),
    _RegularStage("1-1N - Samurai Dubstep", "1-1N", "Main Ward", "Act 1"),
    _RegularStage("1-2 - Intimate", "1-2", "Main Ward", "Act 1"),
    _RegularStage("1-2N - Intimate (Night)", "1-2N", "Main Ward", "Act 1"),
    _RegularStage("1-CNY - Chinese New Year", "1-CNY", "Main Ward", "Act 1"),
    _RegularStage("1-BOO - theme of really spooky bird", "1-BOO", "Main Ward", "Act 1"),
    _RegularStage("3-1 - Sleepy Garden", "3-1", "Main Ward", "Act 3"),
    _RegularStage("3-1N - Lounge", "3-1N", "Main Ward", "Act 3"),
    _RegularStage("3-2 - Classy", "3-2", "Main Ward", "Act 3"),
    _RegularStage("3-2N - Classy (Night)", "3-2N", "Main Ward", "Act 3"),
    _RegularStage("3-3 - Distant Duet", "3-3", "Main Ward", "Act 3"),
    _RegularStage("3-3N - Distant Duet (Night)", "3-3N", "Main Ward", "Act 3"),
]

svt_ward_stages = [
    _RegularStage("2-1 - Lo-fi Hip-Hop Beats To Treat Patients To", "2-1", "SVT Ward", "Act 2"),
    _RegularStage("2-1N - wish i could care less", "2-1N", "SVT Ward", "Act 2"),
    _RegularStage("2-2 - Supraventricular Tachycardia", "2-2", "SVT Ward", "Act 2"),
    _RegularStage("2-2N - Unreachable", "2-2N", "SVT Ward", "Act 2"),
    _RegularStage("2-3 - Puff Piece", "2-3", "SVT Ward", "Act 2"),
    _RegularStage("2-3N - Bomb-Sniffing Pomeranian", "2-3N", "SVT Ward", "Act 2"),
    _RegularStage(
        "2-4 - Song of the Sea", "2-4", "SVT Ward", "Act 2", b_rank_location=False, a_rank_location=False, excluded=True
    ),
    _RegularStage(
        "2-4N - Song of the Sea (Night)",
        "2-4N",
        "SVT Ward",
        "Act 2",
        b_rank_location=False,
        a_rank_location=False,
        excluded=True,
    ),
    _RegularStage("2-B1 - Beans Hopper", "2-B1", "SVT Ward", "Act 2", excluded=False),
]

train_stages = [
    _RegularStage("4-1 - Training Doctor's Train Ride Performance", "4-1", "Train", "Act 4"),
    _RegularStage("4-1N - Rollerdisco Rumble", "4-1N", "Train", "Act 4"),
    _RegularStage("4-2 - Invisible", "4-2", "Train", "Act 4"),
    _RegularStage("4-2N - Invisible (Night)", "4-2N", "Train", "Act 4"),
    _RegularStage("4-3 - Steinway", "4-3", "Train", "Act 4"),
    _RegularStage("4-3N - Steinway Reprise", "4-3N", "Train", "Act 4"),
    _RegularStage("4-4 - Know You", "4-4", "Train", "Act 4"),
    _RegularStage("4-4N - Murmurs", "4-4N", "Train", "Act 4"),
]

physiotherapy_ward_stages = [
    _RegularStage("5-1 - Lucky Break", "5-1", "Physiotherapy Ward", "Act 5"),
    _RegularStage("5-1N - One Slip Too Late", "5-1N", "Physiotherapy Ward", "Act 5"),
    _RegularStage("5-2 - Lo-fi Beats For Patients To Chill To", "5-2", "Physiotherapy Ward", "Act 5"),
    _RegularStage("5-2N - Unsustainable Inconsolable", "5-2N", "Physiotherapy Ward", "Act 5"),
    _RegularStage(
        "5-3 - Seventh Inning Stretch",
        "5-3",
        "Physiotherapy Ward",
        "Act 5",
        b_rank_location=False,
        a_rank_location=False,
        excluded=True,
    ),
    _RhythmWeightlifterStage("5-B1 - Rhythm Weightlifter", "5-B1", "Physiotherapy Ward", "Act 5"),
]

other_stages = [
    _RegularStage("X-FTS - Fixations Towards the Stars", "X-FTS", "Basement", None),
    _RegularStage("X-KOB - Kingdom of Balloons", "X-KOB", "Basement", None),
    _RegularStage("X-WOT - Worn Out Tapes", "X-WOT", "Basement", None),
    _RegularStage("X-MAT - Meet and Tweet", "X-MAT", "Basement", None),
    _RegularStage("MD-1 - Blackest Luxury Car", "MD-1", "Basement", None),
    _RegularStage("MD-2 - tape/stop/night", "MD-2", "Basement", None),
    _RegularStage("MD-3 - The 90's Decision", "MD-3", "Basement", None),
    _RegularStage("X-0 - Helping Hands", "X-0", "Art Room", None),
    _RegularStage("X-1 - Art Exercise", "X-1", "Basement", None),
]
"""
Stages that don't have a corresponding boss song or act.
"""

all_regular_stages = main_ward_stages + svt_ward_stages + train_stages + physiotherapy_ward_stages + other_stages
# endregion

# region Bosses
act_1_boss = _BossStage("1-X - Battleworn Insomniac", "1-X", "Main Ward", "Act 1")
act_2_boss = _BossStage("2-X - All The Times", "2-X", "SVT Ward", "Act 2")
act_3_boss = _BossStage("3-X - One Shift More", "3-X", "Main Ward", "Act 3")
act_3_secret_boss = _BossStage("3-DOG - Rhythm Dogtor", "3-DOG", "Main Ward", "Act 3")
act_4_boss = _BossStage("4-X - Super Battleworn Insomniac", "1-XN", "Main Ward", "Act 4")
act_5_boss = _BossStage("5-X - Dreams Don't Stop", "5-X", "Physiotherapy Ward", "Act 5", clear_plus_location=True)

all_boss_stages = [
    act_1_boss,
    act_2_boss,
    act_3_boss,
    act_3_secret_boss,
    act_4_boss,
    act_5_boss,
]

# endregion

all_stages = all_regular_stages + all_boss_stages


# endregion


def create_items(world: "RhythmDoctorWorld"):
    # Get a random level in the Main Ward to start with
    # At runtime this seems to be a frozenset, not a list (for some reason???)
    start_with_item = world.random.choice(list(world.item_name_groups["Act 1"] | world.item_name_groups["Act 3"]))

    def create_item_from_stage(stage: _RegularStage) -> None:
        item = world.create_item(stage.name)
        if stage.name == start_with_item:
            world.push_precollected(item)
        else:
            item_pool.append(item)

    def create_keys() -> None:
        for ward_name in REGIONS:
            if ward_name == "Main Ward":
                # Main Ward is always accessible
                continue
            if ward_name == "Art Room" and world.options.end_goal.value == EndGoal.option_helping_hands:
                # When Art Room is the end goal, we do not need a key to access it (it will unlock automatically)
                continue

            item_pool.append(world.create_item(f"{ward_name} Key"))

    def pad_with_filler() -> None:
        for _ in range(total_locations - len(item_pool)):
            item_pool.append(world.create_filler())

    total_locations = len(world.multiworld.get_unfilled_locations(world.player))
    item_pool = []

    for stage in all_regular_stages:
        if world.options.end_goal.value == EndGoal.option_helping_hands and stage.short_name == "X-0":
            continue

        create_item_from_stage(stage)
    create_keys()
    pad_with_filler()

    world.multiworld.itempool += item_pool


def create_locations(world: "RhythmDoctorWorld"):
    def create_locations_from_stage(stage: _Stage):
        locations = stage.get_locations(world)
        world.get_region(stage.short_name).add_locations(locations, RhythmDoctorLocation)

        if stage.excluded:
            for location_name in locations.keys():
                world.get_location(location_name).progress_type = LocationProgressType.EXCLUDED
        elif stage.short_name == "5-B1":
            for stage_number in range(5,11):
                world.get_location(f"5-B1 - Rhythm Weightlifter - Stage {stage_number} Clear").progress_type \
                    = LocationProgressType.EXCLUDED
        elif world.options.s_ranks_excluded.value:
            if isinstance(stage, _RegularStage) and stage.s_rank_location:
                world.get_location(f"{stage.name} - S Rank").progress_type = LocationProgressType.EXCLUDED
            elif isinstance(stage, _BossStage) and stage.clear_perfect_location:
                world.get_location(f"{stage.name} - Perfect Clear").progress_type = LocationProgressType.EXCLUDED

    for stage in all_stages:
        if stage.short_name == "X-0" and world.options.end_goal.value == EndGoal.option_helping_hands:
            continue

        create_locations_from_stage(stage)


def get_location_name_to_id() -> dict[str, int]:
    location_name_to_id = {}
    i = 1  # For some reason Archipelago discards i=0

    for stage in all_regular_stages:
        if stage.short_name == "5-B1":
            for stage_number in range(1, 11):
                location_name_to_id[f"{stage.name} - Stage {stage_number} Clear"] = i
                i += 1
        else:
            if stage.b_rank_location:
                location_name_to_id[f"{stage.name} - B Rank"] = i
                i += 1
            if stage.a_rank_location:
                location_name_to_id[f"{stage.name} - A Rank"] = i
                i += 1
            if stage.s_rank_location:
                location_name_to_id[f"{stage.name} - S Rank"] = i
                i += 1

    for stage in all_boss_stages:
        if stage.clear_location:
            location_name_to_id[f"{stage.name} - Clear"] = i
            i += 1
        if stage.clear_plus_location:
            location_name_to_id[f"{stage.name} - Complete+ Without Checkpoints"] = i
            i += 1
        if stage.clear_perfect_location:
            location_name_to_id[f"{stage.name} - Perfect Clear"] = i
            i += 1

    return location_name_to_id


def get_item_name_to_id() -> dict[str, int]:
    item_name_to_id = {}
    # For some reason Archipelago discards i=0
    i = 1

    # Stages
    for stage in all_stages:
        item_name_to_id[stage.name] = i
        i += 1

    # Keys
    for ward_name in REGIONS:
        if ward_name == "Main Ward":
            # Main Ward is always accessible
            continue

        item_name_to_id[f"{ward_name} Key"] = i
        i += 1

    for filler in FILLER:
        item_name_to_id[filler] = i
        i += 1

    return item_name_to_id
