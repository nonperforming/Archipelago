from BaseClasses import MultiWorld, Region, Entrance, CollectionState, LocationProgressType
from .Data import RhythmDoctorLocation, locations_dictionary, get_progress_type
from . import RhythmDoctorWorld
from ..generic.Rules import CollectionRule

wards = list(locations_dictionary["locations"].keys())


def humanize_name(name: str) -> str:
    # "Svt" -> "SVT": the ward in-game is called "SVT Ward", as SVT is an abbreviation
    return name.replace("-", " ").title().replace("Svt", "SVT")


# Code adapted from Saving Princess
def create_regions(multiworld: MultiWorld, player: int) -> None:
    for ward in wards:
        region = Region(humanize_name(ward), player, multiworld)

        # Add related locations to regions
        for level in locations_dictionary["locations"][ward].values():
            for location_dict in level:
                location = RhythmDoctorLocation(player, location_dict["name"], location_dict["id"], region)
                location.progress_type = get_progress_type(location_dict["classification"])
                region.locations.append(location)

        multiworld.regions.append(region)
    connect_regions(multiworld, player)


def connect_regions(multiworld: MultiWorld, player: int) -> None:
    # Add a connection between the Main Menu and Main Ward
    # TODO: cleanup opted to use origin_region_name
    # do we need to do this
    # menu = multiworld.get_region("Menu", player)
    # main = multiworld.get_region("Main Ward", player)
    # connection = Entrance(player, f"Main Ward Entrance", menu)
    # menu.exits.append(connection)
    # connection.connect(main)

    main = multiworld.get_region(RhythmDoctorWorld.origin_region_name, player)

    # Add a connection from the Main Ward to all other wards
    for ward in wards:
        # Don't link the main ward to itself
        if ward == RhythmDoctorWorld.origin_region_name:
            continue

        ward = humanize_name(ward)
        connection = Entrance(player, f"{ward} Entrance", main)
        main.exits.append(connection)
        connection.connect(multiworld.get_region(ward, player))
