from typing import TYPE_CHECKING

from .Data import LEVEL_COUNT_IN_ACT
from .Options import EndGoal

if TYPE_CHECKING:
    from . import RhythmDoctorWorld


def set_rules(world: "RhythmDoctorWorld"):
    # TODO: X-0 with its end goal
    # TODO: Boss level conditions
    level_required_multiplier = 1
    if world.options.boss_unlock_requirement.value == world.options.boss_unlock_requirement.option_clear_half_in_act:
        level_required_multiplier = 0.5

    match world.options.end_goal.value:
        case EndGoal.option_helping_hands:
            # TODO: duplicated in regions
            world.multiworld.completion_condition[world.player] = lambda state: (
                state.has_group("Act 1", world.player, int(LEVEL_COUNT_IN_ACT["Act 1"] * level_required_multiplier))
                and state.has_group("Act 2", world.player, int(LEVEL_COUNT_IN_ACT["Act 2"] * level_required_multiplier))
                and state.has_group("Act 3", world.player, int(LEVEL_COUNT_IN_ACT["Act 3"] * level_required_multiplier))
                and state.has_group("Act 4", world.player, int(LEVEL_COUNT_IN_ACT["Act 4"] * level_required_multiplier))
                and state.has_group("Act 5", world.player, int(LEVEL_COUNT_IN_ACT["Act 5"] * level_required_multiplier))
                and state.has_group("Act 6", world.player, int(LEVEL_COUNT_IN_ACT["Act 6"] * level_required_multiplier))
                and state.has_group("Act 7", world.player, int(LEVEL_COUNT_IN_ACT["Act 7"] * level_required_multiplier))
            )
        case EndGoal.option_perfect_all | EndGoal.option_a_rank_all | EndGoal.option_b_rank_all:
            world.multiworld.completion_condition[world.player] = lambda state: state.has_all(
                world.item_name_groups["Stages"], world.player
            )
