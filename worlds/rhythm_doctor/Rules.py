from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule
from . import RhythmDoctorWorld
from .Data import flattened_items, locations_dictionary


def set_rules(world: RhythmDoctorWorld):
    def has_key(state: CollectionState, area: str) -> bool:
        return state.has(f"{area} Key", world.player)

    def set_key_requirement(yaml_key: str, key: str):
        for level in locations_dictionary["locations"][yaml_key]:
            for location in level:
                set_rule(world.get_location(location["name"]), lambda state: has_key(state, key))

    # Set level item requirement for level locations
    item_index = 0
    for ward_name in locations_dictionary["locations"].keys():
        levels_in_ward = locations_dictionary["locations"][
            ward_name].values()  # FIXME: This is a dict at runtime; why is type checking insisting it is list? Check Data.py!!
        for locations_in_level in levels_in_ward:
            item = flattened_items[item_index := item_index + 1]
            for location in locations_in_level:
                set_rule(world.get_location(location["name"]), lambda state: state.has(item.name, world.player))
    del item_index

    # Set key requirement
    # Act 1/Act 3 are available to the user at all times
    for levels_in_ward in locations_dictionary["locations"].keys():
        region_name = levels_in_ward.replace("-", " ").title()
        if region_name == "Main Ward":  # Helping Hands stays in the world regardless of it being in generation or not.
            # or world.options.end_goal == EndGoal.option_helping_hands and region_name == "Art Room":
            continue
        set_key_requirement(region_name + " Key", region_name)

    # TODO: Saving Princess has a "VICTORY ITEM".
    #       But we are calling SetGoalAchieved() on client plugin, do we need this?
    #       https://archipelagomw.github.io/Archipelago.MultiClient.Net/api/Archipelago.MultiClient.Net.ArchipelagoSession.html#Archipelago_MultiClient_Net_ArchipelagoSession_SetGoalAchieved
