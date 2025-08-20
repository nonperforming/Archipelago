from typing import TYPE_CHECKING

from BaseClasses import Region

from .Data import REGIONS, all_regular_stages, all_boss_stages
from .Options import EndGoal

if TYPE_CHECKING:
    from . import RhythmDoctorWorld


def create_and_connect_regions(world: "RhythmDoctorWorld"):
    create_main_regions(world)
    connect_main_regions(world)
    create_and_connect_stage_regions(world)


def create_main_regions(world: "RhythmDoctorWorld"):
    """
    Create regions for each of the Wards (and Art Room + Basement)
    """
    for region_name in REGIONS:
        region = Region(region_name, world.player, world.multiworld)
        world.multiworld.regions.append(region)


def connect_main_regions(world: "RhythmDoctorWorld"):
    main_ward_region = world.get_region(world.origin_region_name)
    for region_name in REGIONS:
        if region_name == world.origin_region_name:
            continue

        region = world.get_region(region_name)
        rule = (lambda ward: lambda state: state.has(f"{ward} Key", world.player))(region_name)
        main_ward_region.connect(region, f"{world.origin_region_name} to {region_name}", rule)


def create_and_connect_stage_regions(world: "RhythmDoctorWorld"):
    """
    Create and connect regions for each of the standard and boss stages

    Must be run after create_main_regions()
    """
    for stage in all_regular_stages:
        region = world.get_region(stage.region_name)
        stage_region = Region(stage.short_name, world.player, world.multiworld)
        world.multiworld.regions.append(stage_region)

        if stage.short_name == "X-0" and world.options.end_goal.value == EndGoal.option_helping_hands:
            # TODO: duplicated in Rules
            rule = lambda state: (state.has_group("Act 1", world.player, 2) and
                                  state.has_group("Act 2", world.player, 4) and
                                  state.has_group("Act 3", world.player, 3) and
                                  state.has_group("Act 4", world.player, 4) and
                                  state.has_group("Act 5", world.player, 3))
        else:
            rule = (lambda item_name: lambda state: state.has(item_name, world.player))(stage.name)
        region.connect(stage_region, f"{stage.region_name} to {stage.short_name}", rule)

    for boss_stage in all_boss_stages:
        region = world.get_region(boss_stage.region_name)
        stage_region = Region(boss_stage.short_name, world.player, world.multiworld)
        world.multiworld.regions.append(stage_region)

        # TODO: This should be half the levels in the act, doing it automatically instead of hardcoding would be better
        match boss_stage.act:
            case "Act 1":
                requires_count = 2
            case "Act 2":
                requires_count = 4
            case "Act 3":
                requires_count = 3
            case "Act 4":
                requires_count = 4
            case "Act 5":
                requires_count = 3
            case _:
                raise KeyError(f"Rhythm Doctor: Could not find {boss_stage.act}'s requires_count")

        # what?
        # python weirdness: splitting this out here makes things work properly
        rule = ((lambda act, count: lambda state: state.has_group(act, world.player, count))
                (boss_stage.act, requires_count))
        region.connect(stage_region, f"{boss_stage.region_name} to {boss_stage.short_name}", rule)
