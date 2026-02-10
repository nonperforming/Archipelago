from typing import TYPE_CHECKING

from rule_builder.rules import HasAll, HasGroup

from .Options import EndGoal

if TYPE_CHECKING:
    from . import RhythmDoctorWorld


def set_rules(world: "RhythmDoctorWorld"):
    # TODO: X-0 with its end goal
    # TODO: Boss level conditions
    match world.options.end_goal.value:
        case EndGoal.option_helping_hands:
            # TODO: duplicated in regions
            world.set_completion_rule(HasGroup("Act 1", count=world.options.act_1_boss_unlock_requirement.value) \
                   & HasGroup("Act 2", count=world.options.act_2_boss_unlock_requirement.value) \
                   & HasGroup("Act 3", count=world.options.act_3_boss_unlock_requirement.value) \
                   & HasGroup("Act 4", count=world.options.act_4_boss_unlock_requirement.value) \
                   & HasGroup("Act 5", count=world.options.act_5_boss_unlock_requirement.value) \
                   & HasGroup("Act 6", count=world.options.act_6_boss_unlock_requirement.value) \
                   & HasGroup("Act 7", count=world.options.act_7_boss_unlock_requirement.value))
        case EndGoal.option_perfect_all | EndGoal.option_a_rank_all | EndGoal.option_b_rank_all:
            world.set_completion_rule(HasAll(*world.item_name_groups["Stages"]))
