from BaseClasses import CollectionState, Location, MultiWorld
from worlds.generic.Rules import set_rule
from . import RhythmDoctorWorld
from .Data import flattened_items, locations_dictionary
from .Options import EndGoal

def set_rules(world: RhythmDoctorWorld):
    def has_key(state: CollectionState, area: str) -> bool:
        return state.has(f"{area} Key", world.player)

    def set_key_requirement(yaml_key: str, key: str):
        for level in locations_dictionary["locations"][yaml_key]:
            for location in level:
                set_rule(location["name"], lambda state: has_key(state, key))

    # Set level item requirement for level locations
    for items_index, area in enumerate(locations_dictionary["locations"]):
        for level in area:
            item = flattened_items[items_index]
            for location in level:
                # We need to get the corresponding item for these locations
                set_rule(world.multiworld.get_location(location, world.player), lambda state: state.has(item.name))

    # Set key requirement
    # Act 1/Act 3 are available to the user at all times
    for ward in locations_dictionary["locations"].keys():
        region_name = ward.replace("-", " ").title()
        if region_name == "Main Ward" or world.options.end_goal == EndGoal.option_helping_hands and region_name == "Art Room":
            continue
        set_key_requirement(region_name + " Key", region_name)