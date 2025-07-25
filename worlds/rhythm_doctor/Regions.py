from BaseClasses import ItemClassification, MultiWorld, Region, Entrance, CollectionState, LocationProgressType
from .Data import RhythmDoctorItem, RhythmDoctorLocation, locations_dictionary, get_progress_type
from .Options import EndGoal
from . import RhythmDoctorWorld

wards = list(locations_dictionary["locations"].keys())


def humanize_name(name: str) -> str:
    # "Svt" -> "SVT": the ward in-game is called "SVT Ward", as SVT is an abbreviation
    return name.replace("-", " ").title().replace("Svt", "SVT")


# Code adapted from Saving Princess
def create_regions(world: RhythmDoctorWorld, player: int) -> None:
    for ward in wards:
        region = Region(humanize_name(ward), player, world.multiworld)

        # Add related locations to regions
        for level in locations_dictionary["locations"][ward].values():
            for location_dict in level:
                location = RhythmDoctorLocation(player, location_dict["name"], location_dict["id"], region)
                location.progress_type = get_progress_type(location_dict["classification"])
                region.locations.append(location)

        world.multiworld.regions.append(region)
    connect_regions(world.multiworld, player)

    if world.options.end_goal.value == EndGoal.option_helping_hands:
        victory_region = world.multiworld.get_region("Art Room", world.player)
        victory_location = RhythmDoctorLocation(world.player, "X-0 - Helping Hands - Clear", None, victory_region)
        victory_region.locations = [victory_location]
        victory_item = RhythmDoctorItem("Beat X-0 - Helping Hands", None, world.get_region("Art Room"), world.player)
        victory_item.classification = ItemClassification.progression_skip_balancing # Errors if we don't put a classification.
        victory_location.place_locked_item(victory_item)
        world.multiworld.completion_condition[world.player] = lambda state: state.has("Beat X-0 - Helping Hands", world.player)
    else:
        raise NotImplementedError()


def connect_regions(multiworld: MultiWorld, player: int) -> None:
    # Add a connection between the Main Menu and Main Ward
    # TODO: cleanup opted to use origin_region_name
    # do we need to do this
    # menu = multiworld.get_region("Menu", player)
    # main = multiworld.get_region("Main Ward", player)
    # connection = Entrance(player, f"Main Ward Entrance", menu)
    # menu.exits.append(connection)
    # connection.connect(main)

    main_ward_region = multiworld.get_region(RhythmDoctorWorld.origin_region_name, player)
    # Add a connection from the Main Ward to all other wards and back
    for ward in wards:
        # Don't link the main ward to itself
        if ward == RhythmDoctorWorld.origin_region_name:
            continue

        # Add a connection from the main ward to the other ward
        ward_name = humanize_name(ward)
        ward_region = multiworld.get_region(ward_name, player)
        connection = Entrance(player, f"{ward_name} Entrance", main_ward_region)
        main_ward_region.exits.append(connection)
        connection.connect(ward_region)

        # Add a connection from the other ward to the main ward
        ward_region.connect(main_ward_region, f"{ward_name}-Main Ward Entrance")