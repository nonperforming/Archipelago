from BaseClasses import CollectionState, Region
from worlds.generic.Rules import add_rule, set_rule
from . import RhythmDoctorWorld
from .Data import flattened_items, locations_dictionary, RhythmDoctorItem, RhythmDoctorLocation # FIXME: We don't need to repeated deserialize our data. Put it in world somehow.
from .Options import EndGoal
from .Regions import humanize_name

def set_rules(world: RhythmDoctorWorld):
    # TODO: Currently assumes X-0 is the end goal.

    def set_level_item_requirements():
        for ward_name in iter(locations_dictionary["locations"].keys()):
            # FIXME: This is a dict at runtime; why is type checking insisting it is list? Check Data.py!!
            levels_in_ward = locations_dictionary["locations"][ward_name].values()

            for level_index, level in enumerate(levels_in_ward):
                level_name = list(locations_dictionary["locations"][ward_name].keys())[level_index]
                if level_name == "X-0":
                    # X-0 is our end goal - do not add it as a location.
                    continue
                for location in level:
                    item_name = flattened_items[level_index]["name"]
                    set_rule(world.get_location(location["name"]), lambda state: state.has(item_name, world.player))

    def set_key_requirements():
        for ward_name in iter(locations_dictionary["locations"].keys()):
            if ward_name == "Art Room" and world.options.end_goal == EndGoal.art_room:
                # X-0 (as end goal) unlocks when all bosses have been cleared, and does not require a key.
                continue
            elif ward_name == "main-ward":
                # Main Ward requires no key.
                continue
            key_name = f"{humanize_name(ward_name)} Key"
            entrance = world.get_entrance(f"{humanize_name(ward_name)} Entrance")
            set_rule(entrance, lambda state: state.has(key_name, world.player))

    def set_boss_act_requirements():
        # Act 1 (2 levels) - 1-X - Battleworn Insomniac
        add_rule(world.multiworld.get_location("1-X - Battleworn Insomniac - Clear", world.player),
                 lambda state: state.has_group("Act 1 Levels", world.player, 2))
        add_rule(world.multiworld.get_location("1-X - Battleworn Insomniac - Perfect Clear", world.player),
                 lambda state: state.has_group("Act 1 Levels", world.player, 2))
        # Act 2 (4 levels) - 2-X - All The Times
        add_rule(world.multiworld.get_location("2-X - All The Times - Clear", world.player),
                 lambda state: state.has_group("Act 2 Levels", world.player, 4))
        add_rule(world.multiworld.get_location("2-X - All The Times - Perfect Clear", world.player),
                 lambda state: state.has_group("Act 2 Levels", world.player, 4))
        # Act 3 (3 levels) - 3-X - One Shift More
        add_rule(world.multiworld.get_location("3-X - One Shift More - Clear", world.player),
                 lambda state: state.has_group("Act 3 Levels", world.player, 3))
        add_rule(world.multiworld.get_location("3-X - One Shift More - Perfect Clear", world.player),
                 lambda state: state.has_group("Act 3 Levels", world.player, 3))
        # Act 4 (4 levels) - 1-XN - Super Battleworn Insomniac
        add_rule(world.multiworld.get_location("1-XN - Super Battleworn Insomniac - Clear", world.player),
                 lambda state: state.has_group("Act 4 Levels", world.player, 4))
        add_rule(world.multiworld.get_location("1-XN - Super Battleworn Insomniac - Perfect Clear", world.player),
                 lambda state: state.has_group("Act 4 Levels", world.player, 4))
        # Act 5 (3 levels) - 5-X - Dreams Don't Stop
        add_rule(world.multiworld.get_location("5-X - Dreams Don't Stop - Clear", world.player),
                 lambda state: state.has_group("Act 5 Levels", world.player, 3))
        add_rule(world.multiworld.get_location("5-X - Dreams Don't Stop - Checkpointless Clear", world.player),
                 lambda state: state.has_group("Act 5 Levels", world.player, 3))
        add_rule(world.multiworld.get_location("5-X - Dreams Don't Stop - Perfect Clear", world.player),
                 lambda state: state.has_group("Act 5 Levels", world.player, 3))

    set_level_item_requirements()
    set_key_requirements()
    set_boss_act_requirements()

    if world.options.end_goal == EndGoal.option_helping_hands:
        # Only accessible when all bosses have been cleared.
        add_rule(world.multiworld.get_location("X-0 - Helping Hands - Clear", world.player),
                 lambda state: state.has_group("Act 1 Levels", world.player, 2) and
                 state.has_group("Act 2 Levels", world.player, 4) and
                 state.has_group("Act 3 Levels", world.player, 3) and
                 state.has_group("Act 4 Levels", world.player, 4) and
                 state.has_group("Act 5 Levels", world.player, 3))

        victory_event_location =  world.get_location("X-0 - Helping Hands - Clear")
        set_rule(victory_event_location, lambda state: state.has("Beat X-0 - Helping Hands", world.player)) # Must have location clear boss
    else:
        raise NotImplementedError()

    from Utils import visualize_regions
    visualize_regions(world.multiworld.get_region("Main Ward", world.player), "rd.puml")