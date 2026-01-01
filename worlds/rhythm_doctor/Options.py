from dataclasses import dataclass

from Options import (
    Choice,
    DeathLink,
    DefaultOnToggle,
    OptionGroup,
    OptionSet,
    PerGameCommonOptions,
    Range,
    Toggle,
)


# region Options
# region Generation
class EndGoal(Choice):
    """
    The end goal required to beat the game.

    **X-0 - Helping Hands:**
    Clear all other bosses (1-X, 2-X, 3-X, 1-XN, 5-X, 6-X, 7-X, 7-X2) to unlock X-0 - Helping Hands.
    Then, clear X-0 to beat the game!

    **B Rank All Levels:**
    Clear all levels with a B rank or higher to beat the game!

    **A Rank All Levels:**
    Clear all levels with an A rank or higher to beat the game!

    **Perfect All Levels:**
    Clear all levels with an S/Perfect rank to beat the game!
    """

    display_name = "End Goal"

    option_helping_hands = 0
    option_b_rank_all = 1
    option_a_rank_all = 2
    option_perfect_all = 3
    default = 0


class BossUnlockRequirement(Choice):
    """
    The requirements to unlock the boss level for an act.

    **B Rank:**
    The number of levels in their respective act are required to be cleared with a B rank or higher to unlock the act's boss.

    **A Rank:**
    The number of levels in their respective act are required to be cleared with an A rank or higher to unlock the act's boss.

    **Perfect:**
    The number of levels in their respective act are required to be cleared with an S/Perfect rank to unlock the act's boss.
    """

    display_name = "Boss Unlock Requirement"

    option_b_rank = 0
    option_a_rank = 1
    option_perfect = 2
    default = 0


class Act1BossUnlockRequirement(Range):
    """
    The number of levels required to be cleared (with the rank set in Boss Unlock Requirement) to unlock '1-X - Battleworn Insomniac'.

    This includes '1-BOO - theme of really spooky bird' and '1-CNY - Chinese New Year'.
    """

    display_name = "Act 1 Boss Unlock Requirement"

    range_start = 1
    range_end = 6
    default = 2


class Act2BossUnlockRequirement(Range):
    """
    The number of levels required to be cleared (with the rank set in Boss Unlock Requirement) to unlock '2-X - All The Times'.

    This includes '2-B1 - Beans Hopper', but **does not** include '2-XN - Bitter Times'.
    """

    display_name = "Act 2 Boss Unlock Requirement"

    range_start = 1
    range_end = 9
    default = 4


class Act3BossUnlockRequirement(Range):
    """
    The number of levels required to be cleared (with the rank set in Boss Unlock Requirement) to unlock '3-X - One Shift More'.
    """

    display_name = "Act 3 Boss Unlock Requirement"

    range_start = 1
    range_end = 6
    default = 3


class Act4BossUnlockRequirement(Range):
    """
    The number of levels required to be cleared (with the rank set in Boss Unlock Requirement) to unlock '1-XN - Super Battleworn Insomniac'.
    """

    display_name = "Act 4 Boss Unlock Requirement"

    range_start = 1
    range_end = 8
    default = 4


class Act5BossUnlockRequirement(Range):
    """
    The number of levels required to be cleared (with the rank set in Boss Unlock Requirement) to unlock 5-X - Dreams Don't Stop.

    This includes '5-3 - Seventh-Inning Stretch', but **does not** include '5-B1 - Rhythm Weightlifter'.
    """

    display_name = "Act 5 Boss Unlock Requirement"

    range_start = 1
    range_end = 6
    default = 3


class Act6BossUnlockRequirement(Range):
    """
    The number of levels required to be cleared (with the rank set in Boss Unlock Requirement) to unlock '6-X - Boss Fight'.
    """

    display_name = "Act 6 Boss Unlock Requirement"

    range_start = 1
    range_end = 2
    default = 2


class Act7BossUnlockRequirement(Range):
    """
    The number of levels required to be cleared (with the rank set in Boss Unlock Requirement) to unlock the Abandoned Ward and '7-X - Miracle Defibrillator', '7-X2 - Miracle Defibrillator (Cole's Song)'.

    This includes '2-XN - Bitter Times'.
    """

    display_name = "Act 7 Boss Unlock Requirement"

    range_start = 1
    range_end = 2
    default = 2


class PerfectRanksExcluded(DefaultOnToggle):
    """Determines if Perfect/S rank locations are excluded in generation."""

    display_name = "Exclude Perfect Ranks"


# endregion


# region Gameplay
# region Traps
class TrapChance(Range):
    """Determines the percent likeliness of a **filler item becoming a trap**.
    **The sum of Trap Chance and Powerup Chance cannot be over 100%.**"""

    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 0


class EnableFragileHeartTraps(Toggle):
    """Determines if **increased mistake weight traps** should be in the item pool."""

    display_name = "Enable Fragile Heart Traps"


class EnableCharacterScrambleTraps(Toggle):
    """Determines if **randomized characters traps** should be in the item pool."""

    display_name = "Enable Character Scramble Traps"


class EnableBeatsoundScrambleTraps(Toggle):
    """Determines if **randomized beatsound traps** should be in the item pool."""

    display_name = "Enable Beatsound Scramble Traps"


class EnableHitsoundScrambleTraps(Toggle):
    """Determines if **randomized hitsound traps** should be in the item pool."""

    display_name = "Enable Hitsound Scramble Traps"


class EnableHardDifficultyTraps(Toggle):
    """Determines if **hard difficulty traps** should be in the item pool."""

    display_name = "Enable Hard Difficulty Traps"


class EnableChilliSpeedTraps(Toggle):
    """Determines if **🌶️ chilli speed traps** should be in the item pool."""

    display_name = "Enable Chilli Speed Traps"


class EnableGhostTapTraps(Toggle):
    """Determines if **ghost tap traps** (make a mistake on ghost tap) should be in the item pool."""

    display_name = "Enable Ghost Tap Traps"


class StickyTraps(OptionSet):
    """Determines the **set of traps that should be applied wherever possible**."""

    display_name = "Sticky Traps"
    valid_keys = ["Scramble Characters", "Scramble Beatsounds", "Scramble Hitsounds", "Ghost Tap"]


# endregion


# region Powerups
class PowerupChance(Range):
    """Determines the percent likeliness of a **filler item becoming a powerup**.
    **The sum of Trap Chance and Powerup Chance cannot be over 100%.**"""

    display_name = "Powerup Chance"
    range_start = 0
    range_end = 100
    default = 0


class EnableEasyDifficultyPowerups(Toggle):
    """Determines if **easy difficulty powerups** should be in the item pool."""

    display_name = "Enable Easy Difficulty Powerups"


class EnableStrongHeartPowerups(Toggle):
    """Determines if **decreased mistake weight powerups** should be in the item pool."""

    display_name = "Enable Strong Heart Powerups"


class EnableIceSpeedPowerups(Toggle):
    """Determines if **🧊 ice speed powerups** should be in the item pool."""

    display_name = "Enable Ice Speed Powerups"


# Currently we do not have any powerups that could be applied here.
# class StickyPowerups(OptionSet):
#    """Determines the **set of powerups that should be applied wherever possible**."""
#
#    display_name = "Sticky Powerups"
#    valid_keys = [""]
# endregion


class RhythmDoctorDeathLink(DeathLink):
    """
    When you die (a patient's heart breaks), everyone dies. The reverse is also true.

    This can be changed in-game, using the Archipelago page in the pause menu.
    """


# endregion
# endregion


@dataclass
class RhythmDoctorOptions(PerGameCommonOptions):
    # Generation options
    end_goal: EndGoal
    boss_unlock_requirement: BossUnlockRequirement
    act_1_boss_unlock_requirement: Act1BossUnlockRequirement
    act_2_boss_unlock_requirement: Act2BossUnlockRequirement
    act_3_boss_unlock_requirement: Act3BossUnlockRequirement
    act_4_boss_unlock_requirement: Act4BossUnlockRequirement
    act_5_boss_unlock_requirement: Act5BossUnlockRequirement
    act_6_boss_unlock_requirement: Act6BossUnlockRequirement
    act_7_boss_unlock_requirement: Act7BossUnlockRequirement
    perfect_ranks_excluded: PerfectRanksExcluded

    # Gameplay options
    trap_chance: TrapChance
    enable_fragile_heart_traps: EnableFragileHeartTraps
    enable_character_scramble_traps: EnableCharacterScrambleTraps
    enable_beatsound_scramble_traps: EnableBeatsoundScrambleTraps
    enable_hitsound_scramble_traps: EnableHitsoundScrambleTraps
    enable_hard_difficulty_traps: EnableHardDifficultyTraps
    enable_chilli_speed_traps: EnableChilliSpeedTraps
    enable_ghost_tap_traps: EnableGhostTapTraps
    sticky_traps: StickyTraps
    powerup_chance: PowerupChance
    enable_easy_difficulty_powerups: EnableEasyDifficultyPowerups
    enable_strong_heart_powerups: EnableStrongHeartPowerups
    enable_ice_speed_powerups: EnableIceSpeedPowerups
    # sticky_powerups: StickyPowerups
    death_link: RhythmDoctorDeathLink


groups: list[OptionGroup] = [
    OptionGroup(
        "Generation Options",
        [
            EndGoal,
            BossUnlockRequirement,
            Act1BossUnlockRequirement,
            Act2BossUnlockRequirement,
            Act3BossUnlockRequirement,
            Act4BossUnlockRequirement,
            Act5BossUnlockRequirement,
            Act6BossUnlockRequirement,
            Act7BossUnlockRequirement,
            PerfectRanksExcluded,
        ],
    ),
    OptionGroup(
        "Gameplay Options",
        [
            RhythmDoctorDeathLink,
        ],
    ),
    OptionGroup(
        "Trap Options",
        [
            TrapChance,
            EnableFragileHeartTraps,
            EnableCharacterScrambleTraps,
            EnableBeatsoundScrambleTraps,
            EnableHitsoundScrambleTraps,
            EnableHardDifficultyTraps,
            EnableChilliSpeedTraps,
            EnableGhostTapTraps,
            StickyTraps,
        ],
    ),
    OptionGroup(
        "Powerup Options",
        [
            PowerupChance,
            EnableEasyDifficultyPowerups,
            EnableStrongHeartPowerups,
            EnableIceSpeedPowerups,
            # StickyPowerups,
        ],
    ),
]

presets = {
    "Traps & Powerups": {
        "end_goal": EndGoal.option_helping_hands,
        "boss_unlock_requirement": BossUnlockRequirement.default,
        "act_1_boss_unlock_requirement": Act1BossUnlockRequirement.default,
        "act_2_boss_unlock_requirement": Act2BossUnlockRequirement.default,
        "act_3_boss_unlock_requirement": Act3BossUnlockRequirement.default,
        "act_4_boss_unlock_requirement": Act4BossUnlockRequirement.default,
        "act_5_boss_unlock_requirement": Act5BossUnlockRequirement.default,
        "act_6_boss_unlock_requirement": Act6BossUnlockRequirement.default,
        "act_7_boss_unlock_requirement": Act7BossUnlockRequirement.default,
        "perfect_ranks_excluded": True,
        "trap_chance": 33,
        "enable_fragile_heart_traps": True,
        "enable_character_scramble_traps": True,
        "enable_beatsound_scramble_traps": True,
        "enable_hitsound_scramble_traps": True,
        "enable_hard_difficulty_traps": True,
        "enable_chilli_speed_traps": True,
        "enable_ghost_tap_traps": True,
        "sticky_traps": StickyTraps.default,
        "powerup_chance": 33,
        "enable_easy_difficulty_powerups": True,
        "enable_strong_heart_powerups": True,
        "enable_ice_speed_powerups": True,
        # "sticky_powerups": StickyPowerups.default,
        "death_link": False,
    },
}
