from typing import TYPE_CHECKING

from BaseClasses import Region

from .Data import REGIONS, all_regular_stages, all_boss_stages

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

        main_ward_region.connect(region, f"{world.origin_region_name} to {region_name}")
        # lambda state, local_region_name=region_name: state.has(f"{local_region_name} Key", world.player)


def create_and_connect_stage_regions(world: "RhythmDoctorWorld"):
    """
    Create and connect regions for each of the standard and boss stages

    Must be run after create_main_regions()
    """
    for stage in all_regular_stages:
        region = world.get_region(stage.region_name)
        stage_region = Region(stage.short_name, world.player, world.multiworld)
        world.multiworld.regions.append(stage_region)

        region.connect(stage_region, f"{stage.region_name} to {stage.short_name}")
        # lambda state, local_item_name=stage.name: state.has(local_item_name, world.player))

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
        region.connect(stage_region, f"{boss_stage.region_name} to {boss_stage.short_name}")
        # lambda state, local_act=boss_stage.act, local_requires_count=requires_count: state.has_group(local_act, world.player, local_requires_count))

    def connect_regions(world: "RhythmDoctorWorld"):
        main_ward = world.get_region("Main Ward")

        for region_name in REGIONS:
            if region_name == "Main Ward":
                # Do not link the Main Ward to itself
                continue

            region = world.get_region(region_name)
            # TODO: Add entrance rule later. Under certain conditions certain wards like the Art Room will not have a key
            main_ward.connect(region, f"Main Ward to {region_name}")  # , lambda state: state.has(f"{region_name} Key"))
