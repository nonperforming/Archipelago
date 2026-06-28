from typing import TYPE_CHECKING, Literal

from BaseClasses import Region
from rule_builder.field_resolvers import FromOption
from rule_builder.options import OptionFilter
from rule_builder.rules import CanReachEntrance, Has, HasGroup

from .Data import HELPING_HANDS_STAGE, REGIONS, ALL_BOSS_STAGES, ALL_REGULAR_STAGES
from .Options import (
    EndGoal,
    Act3BossUnlockRequirement,
    Act2BossUnlockRequirement,
    Act4BossUnlockRequirement,
    Act5BossUnlockRequirement,
    Act6BossUnlockRequirement,
    Act7BossUnlockRequirement,
)
from .Rules import get_completion_rule_for_helping_hands
from .Options import Act1BossUnlockRequirement

if TYPE_CHECKING:
    from . import RhythmDoctorWorld


def create_and_connect_regions(world: "RhythmDoctorWorld"):
    create_main_regions(world)
    connect_main_regions(world)
    create_and_connect_stage_regions(world)


def create_main_regions(world: "RhythmDoctorWorld"):
    """
    Create regions for each of the Wards (and Garden Room + Basement)
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

        if region_name == "Garden Room":
            world.set_rule(entrance, Has(f"{region_name} Key") | OptionFilter(EndGoal, EndGoal.option_helping_hands))
        else:
            world.set_rule(entrance, Has(f"{region_name} Key"))


def create_and_connect_stage_regions(world: "RhythmDoctorWorld"):
    """
    Create and connect regions for each of the standard and boss stages

    Must be run after create_main_regions()
    """

    def get_boss_unlock_requirement_value_for_act(
        act: Literal["Act 1", "Act 2", "Act 3", "Act 4", "Act 5", "Act 6", "Act 7"],
    ) -> FromOption:
        match act:
            case "Act 1":
                return FromOption(Act1BossUnlockRequirement)
            case "Act 2":
                return FromOption(Act2BossUnlockRequirement)
            case "Act 3":
                return FromOption(Act3BossUnlockRequirement)
            case "Act 4":
                return FromOption(Act4BossUnlockRequirement)
            case "Act 5":
                return FromOption(Act5BossUnlockRequirement)
            case "Act 6":
                return FromOption(Act6BossUnlockRequirement)
            case "Act 7":
                return FromOption(Act7BossUnlockRequirement)
            case _:
                raise NotImplementedError

    for stage in ALL_REGULAR_STAGES:
        # Add stage and its region
        if stage.region_name is None:
            if stage.short_name == "X-1":
                if world.options.end_goal.value == EndGoal.option_helping_hands:
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

        # Set rules
        if world.options.end_goal.value == EndGoal.option_helping_hands and stage.name == HELPING_HANDS_STAGE.name:
            # This is the rule to unlock X-0 with it as the end goal.
            # The completion rule is handled in Rules.py.
            rule = get_completion_rule_for_helping_hands()
        else:
            rule = Has(stage.name)
        entrance = region.connect(stage_region, f"{stage.region_name} to {stage.short_name}")
        world.set_rule(entrance, rule)  # Key rule is handled by the region

    for boss_stage in ALL_BOSS_STAGES:
        region = world.get_region(boss_stage.region_name)  # noqa: no boss stages have special region cases
        stage_region = Region(boss_stage.short_name, world.player, world.multiworld)
        world.multiworld.regions.append(stage_region)

        entrance = region.connect(stage_region, f"{boss_stage.region_name} to {boss_stage.short_name}")
        rule = HasGroup(boss_stage.act, count=get_boss_unlock_requirement_value_for_act(boss_stage.act))  # noqa: all boss stages have act
        if boss_stage.region_name != world.origin_region_name:
            rule = rule & Has(f"{boss_stage.region_name} Key")

        # Stage-specific additional rules
        if boss_stage.short_name == "1-XN":
            # 1-XN is in the Main Ward but requires levels from the Train
            rule = rule & Has("Train Key")
        elif boss_stage.short_name == "7-X":
            # 7-X is in the "Main Ward" but requires at least one level/both "2-XN" and "7-1"
            # from the SVT Ward or Records Room respectively

            # TODO: There should be a better way to do this! This will break when more levels are added to Act 7

            bitter_times_rule = CanReachEntrance("SVT Ward to 2-XN")
            blurred_rule = CanReachEntrance("Records Room to 7-1")
            if get_boss_unlock_requirement_value_for_act("Act 7").resolve(world) == 1:
                rule = rule & (bitter_times_rule | blurred_rule)
            else:
                rule = rule & bitter_times_rule & blurred_rule
        elif boss_stage.short_name == "7-X2":
            # To reach 7-X2 you must first clear 7-X.
            rule = CanReachEntrance("Main Ward to 7-X")
        world.set_rule(entrance, rule)
