from typing import TYPE_CHECKING

from BaseClasses import Region

from .Data import REGIONS, all_boss_stages, all_regular_stages, LEVEL_COUNT_IN_ACT
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

        level_required_multiplier = 1
        if (
            world.options.boss_unlock_requirement.value
            == world.options.boss_unlock_requirement.option_clear_half_in_act
        ):
            level_required_multiplier = 0.5

        if stage.short_name == "X-0" and world.options.end_goal.value == EndGoal.option_helping_hands:
            # TODO: duplicated in Rules
            rule = lambda state: (
                state.has_group("Act 1", world.player, int(LEVEL_COUNT_IN_ACT["Act 1"] * level_required_multiplier))
                and state.has_group("Act 2", world.player, int(LEVEL_COUNT_IN_ACT["Act 2"] * level_required_multiplier))
                and state.has_group("Act 3", world.player, int(LEVEL_COUNT_IN_ACT["Act 3"] * level_required_multiplier))
                and state.has_group("Act 4", world.player, int(LEVEL_COUNT_IN_ACT["Act 4"] * level_required_multiplier))
                and state.has_group("Act 5", world.player, int(LEVEL_COUNT_IN_ACT["Act 5"] * level_required_multiplier))
                and state.has_group("Act 6", world.player, int(LEVEL_COUNT_IN_ACT["Act 6"] * level_required_multiplier))
                and state.has_group("Act 7", world.player, int(LEVEL_COUNT_IN_ACT["Act 7"] * level_required_multiplier))
            )
        else:
            rule = (lambda item_name: lambda state: state.has(item_name, world.player))(stage.name)
        region.connect(stage_region, f"{stage.region_name} to {stage.short_name}", rule)

    for boss_stage in all_boss_stages:
        region = world.get_region(boss_stage.region_name)
        stage_region = Region(boss_stage.short_name, world.player, world.multiworld)
        world.multiworld.regions.append(stage_region)

        level_required_multiplier = 1
        if (
            world.options.boss_unlock_requirement.value
            == world.options.boss_unlock_requirement.option_clear_half_in_act
        ):
            level_required_multiplier = 0.5

        # what?
        # python weirdness: splitting this out here makes things work properly
        rule = (lambda act, count: lambda state: state.has_group(act, world.player, count))(
            boss_stage.act,
            int(LEVEL_COUNT_IN_ACT[boss_stage.act] * level_required_multiplier),  # Python will truncate
        )
        region.connect(stage_region, f"{boss_stage.region_name} to {boss_stage.short_name}", rule)
