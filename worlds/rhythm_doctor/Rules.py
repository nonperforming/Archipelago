from typing import TYPE_CHECKING

from .Options import EndGoal

if TYPE_CHECKING:
    from . import RhythmDoctorWorld


def set_rules(world: "RhythmDoctorWorld"):
    # TODO: X-0 with its end goal
    # TODO: Boss level conditions
    match world.options.end_goal.value:
        case EndGoal.option_helping_hands:
            # TODO: duplicated in regions
            world.multiworld.completion_condition[world.player] = lambda state: (
                state.has_group("Act 1", world.player, world.options.act_1_boss_unlock_requirement.value)
                and state.has_group("Act 2", world.player, world.options.act_2_boss_unlock_requirement.value)
                and state.has_group("Act 3", world.player, world.options.act_3_boss_unlock_requirement.value)
                and state.has_group("Act 4", world.player, world.options.act_4_boss_unlock_requirement.value)
                and state.has_group("Act 5", world.player, world.options.act_5_boss_unlock_requirement.value)
                and state.has_group("Act 6", world.player, world.options.act_6_boss_unlock_requirement.value)
                and state.has_group("Act 7", world.player, world.options.act_7_boss_unlock_requirement.value)
            )
        case EndGoal.option_perfect_all | EndGoal.option_a_rank_all | EndGoal.option_b_rank_all:
            world.multiworld.completion_condition[world.player] = lambda state: state.has_all(
                world.item_name_groups["Stages"], world.player
            )
