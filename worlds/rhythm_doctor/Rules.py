from typing import TYPE_CHECKING

from rule_builder.field_resolvers import FromOption
from rule_builder.options import OptionFilter
from rule_builder.rules import HasAll, HasGroup

from .Data import ALL_PROGRESSION_ITEMS, STORY_KEYS
from .Options import (
    Act1BossUnlockRequirement,
    Act2BossUnlockRequirement,
    Act3BossUnlockRequirement,
    Act4BossUnlockRequirement,
    Act5BossUnlockRequirement,
    Act6BossUnlockRequirement,
    Act7BossUnlockRequirement,
    EndGoal,
)

if TYPE_CHECKING:
    from . import RhythmDoctorWorld


def get_completion_rule_for_helping_hands():
    return (
        HasGroup(
            "Act 1",
            count=FromOption(Act1BossUnlockRequirement),
            options=[OptionFilter(EndGoal, EndGoal.option_helping_hands)],
            filtered_resolution=False,
        )
        & HasGroup(
            "Act 2",
            count=FromOption(Act2BossUnlockRequirement),
            options=[OptionFilter(EndGoal, EndGoal.option_helping_hands)],
            filtered_resolution=False,
        )
        & HasGroup(
            "Act 3",
            count=FromOption(Act3BossUnlockRequirement),
            options=[OptionFilter(EndGoal, EndGoal.option_helping_hands)],
            filtered_resolution=False,
        )
        & HasGroup(
            "Act 4",
            count=FromOption(Act4BossUnlockRequirement),
            options=[OptionFilter(EndGoal, EndGoal.option_helping_hands)],
            filtered_resolution=False,
        )
        & HasGroup(
            "Act 5",
            count=FromOption(Act5BossUnlockRequirement),
            options=[OptionFilter(EndGoal, EndGoal.option_helping_hands)],
            filtered_resolution=False,
        )
        & HasGroup(
            "Act 6",
            count=FromOption(Act6BossUnlockRequirement),
            options=[OptionFilter(EndGoal, EndGoal.option_helping_hands)],
            filtered_resolution=False,
        )
        & HasGroup(
            "Act 7",
            count=FromOption(Act7BossUnlockRequirement),
            options=[OptionFilter(EndGoal, EndGoal.option_helping_hands)],
            filtered_resolution=False,
        )
        & HasAll(
            *[key.name for key in STORY_KEYS],
            options=[OptionFilter(EndGoal, EndGoal.option_helping_hands)],
            filtered_resolution=False,
        )
    )


def set_rules(world: "RhythmDoctorWorld"):
    helping_hands_rule = get_completion_rule_for_helping_hands()
    clear_all_rule = HasAll(
        *[item.name for item in ALL_PROGRESSION_ITEMS],
        options=[OptionFilter(EndGoal, EndGoal.option_helping_hands, "ne")],
        filtered_resolution=False,
    )
    world.set_completion_rule(helping_hands_rule | clear_all_rule)
