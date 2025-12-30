from typing import TYPE_CHECKING

from BaseClasses import Region

from .Data import REGIONS, all_boss_stages, all_regular_stages
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

    def get_boss_unlock_requirement_value_for_act(act: str):
        match act:
            case "Act 1":
                return world.options.act_1_boss_unlock_requirement.value
            case "Act 2":
                return world.options.act_2_boss_unlock_requirement.value
            case "Act 3":
                return world.options.act_3_boss_unlock_requirement.value
            case "Act 4":
                return world.options.act_4_boss_unlock_requirement.value
            case "Act 5":
                return world.options.act_5_boss_unlock_requirement.value
            case "Act 6":
                return world.options.act_6_boss_unlock_requirement.value
            case "Act 7":
                return world.options.act_7_boss_unlock_requirement.value
            case _:
                raise NotImplementedError

    for stage in all_regular_stages:
        region = world.get_region(stage.region_name)
        stage_region = Region(stage.short_name, world.player, world.multiworld)
        world.multiworld.regions.append(stage_region)

        if stage.short_name == "X-0" and world.options.end_goal.value == EndGoal.option_helping_hands:
            # TODO: duplicated in Rules
            rule = lambda state: (
                state.has_group("Act 1", world.player, world.options.act_1_boss_unlock_requirement.value)
                and state.has_group("Act 2", world.player, world.options.act_2_boss_unlock_requirement.value)
                and state.has_group("Act 3", world.player, world.options.act_3_boss_unlock_requirement.value)
                and state.has_group("Act 4", world.player, world.options.act_4_boss_unlock_requirement.value)
                and state.has_group("Act 5", world.player, world.options.act_5_boss_unlock_requirement.value)
                and state.has_group("Act 6", world.player, world.options.act_6_boss_unlock_requirement.value)
                and state.has_group("Act 7", world.player, world.options.act_7_boss_unlock_requirement.value)
            )
        else:
            rule = (lambda item_name: lambda state: state.has(item_name, world.player))(stage.name)
        region.connect(stage_region, f"{stage.region_name} to {stage.short_name}", rule)

    for boss_stage in all_boss_stages:
        region = world.get_region(boss_stage.region_name)
        stage_region = Region(boss_stage.short_name, world.player, world.multiworld)
        world.multiworld.regions.append(stage_region)

        # what?
        # python weirdness: splitting this out here makes things work properly
        rule = (lambda act, count: lambda state: state.has_group(act, world.player, count))(
            boss_stage.act,
            get_boss_unlock_requirement_value_for_act(boss_stage.act),
        )
        region.connect(stage_region, f"{boss_stage.region_name} to {boss_stage.short_name}", rule)
