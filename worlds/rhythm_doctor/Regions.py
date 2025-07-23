from BaseClasses import MultiWorld, Region, Entrance
from .Data import RhythmDoctorLocation, locations_dictionary
from . import RhythmDoctorWorld

wards = list(locations_dictionary["locations"].keys())


def humanize_name(name: str) -> str:
    return name.replace("-", " ").title()


# Code adapted from Saving Princess
def create_regions(multiworld: MultiWorld, player: int) -> None:
    for ward in wards:
        region = Region(humanize_name(ward), player, multiworld)

        # Add related locations to regions
        for level in locations_dictionary["locations"][ward].values():
            for location in level:
                # Classification where?
                region.locations.append(RhythmDoctorLocation(player, location["name"]))

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
