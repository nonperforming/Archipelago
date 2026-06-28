from typing import TYPE_CHECKING

from rule_builder.field_resolvers import FromOption
from rule_builder.options import OptionFilter
from rule_builder.rules import HasAll, HasGroup
from .Data import STORY_KEYS, ALL_PROGRESSION_ITEMS
from .Options import (Act1BossUnlockRequirement, Act2BossUnlockRequirement, Act3BossUnlockRequirement,
                      Act4BossUnlockRequirement, Act5BossUnlockRequirement, Act6BossUnlockRequirement,
                      Act7BossUnlockRequirement, EndGoal)

if TYPE_CHECKING:
    from . import RhythmDoctorWorld


def get_completion_rule_for_helping_hands():
    return (
        HasGroup("Act 1", count=FromOption(Act1BossUnlockRequirement))
        & HasGroup("Act 2", count=FromOption(Act2BossUnlockRequirement))
        & HasGroup("Act 3", count=FromOption(Act3BossUnlockRequirement))
        & HasGroup("Act 4", count=FromOption(Act4BossUnlockRequirement))
        & HasGroup("Act 5", count=FromOption(Act5BossUnlockRequirement))
        & HasGroup("Act 6", count=FromOption(Act6BossUnlockRequirement))
        & HasGroup("Act 7", count=FromOption(Act7BossUnlockRequirement))
        & HasAll(*[key.name for key in STORY_KEYS])
    )



def set_rules(world: "RhythmDoctorWorld"):
    helping_hands_rule = OptionFilter(EndGoal, EndGoal.option_helping_hands) & get_completion_rule_for_helping_hands()
    # can't use '|' operator for OptionFilter, this will have to do for now
    clear_all_rule = OptionFilter(EndGoal, EndGoal.option_helping_hands, "ne") & HasAll(*[item.name for item in ALL_PROGRESSION_ITEMS])
    world.set_completion_rule(helping_hands_rule | clear_all_rule)