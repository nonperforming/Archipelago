from typing import TYPE_CHECKING

from .Options import EndGoal

if TYPE_CHECKING:
    from . import RhythmDoctorWorld


def set_rules(world: "RhythmDoctorWorld"):
    # TODO: X-0 with its end goal
    # TODO: Boss level conditions
    match world.options.end_goal.value:
        case EndGoal.option_helping_hands:
            # TODO: unhardcode
            # TODO: duplicated in regions
            world.multiworld.completion_condition[world.player] = lambda state: (
                state.has_group("Act 1", world.player, 2)
                and state.has_group("Act 2", world.player, 4)
                and state.has_group("Act 3", world.player, 3)
                and state.has_group("Act 4", world.player, 4)
                and state.has_group("Act 5", world.player, 3)
            )
        case EndGoal.option_perfect_all | EndGoal.option_a_rank_all | EndGoal.option_b_rank_all:
            world.multiworld.completion_condition[world.player] = lambda state: state.has_all(
                world.item_name_groups["Stages"], world.player
            )
