from typing import TYPE_CHECKING, Literal

from BaseClasses import Region
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasGroup, CanReachEntrance

from .Data import REGIONS, all_boss_stages, all_regular_stages
from .Options import EndGoal, Act7BossUnlockRequirement

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
        entrance = main_ward_region.connect(region, f"{world.origin_region_name} to {region_name}")

        if region_name == "Garden Room" and OptionFilter(EndGoal, EndGoal.option_helping_hands, "ne"):
            world.set_rule(entrance, Has(f"{region_name} Key"))


def create_and_connect_stage_regions(world: "RhythmDoctorWorld"):
    """
    Create and connect regions for each of the standard and boss stages

    Must be run after create_main_regions()
    """

    def get_boss_unlock_requirement_value_for_act(act: Literal["Act 1", "Act 2", "Act 3", "Act 4", "Act 5", "Act 6", "Act 7"]):
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
        if stage.region_name is None:
            if stage.short_name == "X-1":
                if OptionFilter(EndGoal, EndGoal.option_helping_hands):
                    region = world.get_region("Basement")
                else:
                    region = world.get_region("Garden Room")
            else:
                err = f"Region name for {stage.short_name} is none and does not have special definition defined"
                raise NotImplementedError(err)
        else:
            region = world.get_region(stage.region_name)
        stage_region = Region(stage.short_name, world.player, world.multiworld)
        world.multiworld.regions.append(stage_region)

        if OptionFilter(EndGoal, EndGoal.option_helping_hands) and stage.short_name == "X-0":
            # TODO: duplicated in Rules
            rule = HasGroup("Act 1", count=world.options.act_1_boss_unlock_requirement.value) \
                   & HasGroup("Act 2", count=world.options.act_2_boss_unlock_requirement.value) \
                   & CanReachEntrance(f"{world.origin_region_name} to SVT Ward") \
                   & HasGroup("Act 3", count=world.options.act_3_boss_unlock_requirement.value) \
                   & HasGroup("Act 4", count=world.options.act_4_boss_unlock_requirement.value) \
                   & CanReachEntrance(f"{world.origin_region_name} to Train") \
                   & HasGroup("Act 5", count=world.options.act_5_boss_unlock_requirement.value) \
                   & CanReachEntrance(f"{world.origin_region_name} to Physiotherapy Ward") \
                   & HasGroup("Act 6", count=world.options.act_6_boss_unlock_requirement.value) \
                   & CanReachEntrance(f"{world.origin_region_name} to Records Room") \
                   & HasGroup("Act 7", count=world.options.act_7_boss_unlock_requirement.value)
        else:
            rule = Has(stage.name)
        entrance = region.connect(stage_region, f"{stage.region_name} to {stage.short_name}")
        world.set_rule(entrance, rule) # Key rule is handled by the region

    for boss_stage in all_boss_stages:
        region = world.get_region(boss_stage.region_name)  # noqa: no boss stages have special region cases
        stage_region = Region(boss_stage.short_name, world.player, world.multiworld)
        world.multiworld.regions.append(stage_region)

        entrance = region.connect(stage_region, f"{boss_stage.region_name} to {boss_stage.short_name}")
        rule = HasGroup(boss_stage.act, get_boss_unlock_requirement_value_for_act(boss_stage.act))   # noqa: all boss stages have act
        if boss_stage.region_name != world.origin_region_name:
            rule = rule & Has(f"{boss_stage.region_name} Key")

        if boss_stage.short_name == "1-XN":
            rule = rule & Has("Train Key")
        elif boss_stage.short_name == "7-X":
            # TODO: There should be a better way to do this! This will break when more levels are added to Act 7
            # Due to 7-X being considered in Main Ward while requiring levels in either/both SVT Ward and
            # Records Room to unlock, it must be considered for here.

            bitter_times_rule = CanReachEntrance("SVT Ward to 2-XN")
            blurred_rule = CanReachEntrance("Records Room to 7-1")
            if get_boss_unlock_requirement_value_for_act("Act 7") == 1:
                rule = rule & (bitter_times_rule | blurred_rule)
            else:
                rule = rule & bitter_times_rule & blurred_rule
        elif boss_stage.short_name == "7-X2":
            # To reach 7-X2 you must first clear 7-X.
            rule = CanReachEntrance("Main Ward to 7-X")
        world.set_rule(entrance, rule)
