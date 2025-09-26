from dataclasses import dataclass

from Options import (
    Choice,
    DeathLink,
    DefaultOnToggle,
    OptionGroup,
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
    Clear all other bosses (1-X, 2-X, 3-X, 1-XN, 5-X) to unlock X-0 - Helping Hands.
    Then, clear X-0 to beat the game!

    **B Rank All Levels:**
    Clear all levels with a B rank or higher to beat the game!

    **A Rank All Levels:**
    Clear all levels with an A rank or higher to beat the game!

    **Perfect All Levels:**
    Clear all levels with an S+/Perfect rank to beat the game!
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

    **Clear Half In Act:**
    Only half the number of levels in the act (rounding down if odd) are required to be cleared with a B rank or higher to unlock the act's boss.

    **B Rank All:**
    All the number of levels in the act are required to be cleared with a B rank or higher to unlock the act's boss.

    **A Rank All:**
    All the number of levels in the act are required to be cleared with an A rank or higher to unlock the act's boss.

    **Perfect All:**
    All the number of levels in the act are required to be cleared with an S+ rank to unlock the act's boss.
    """

    display_name = "Boss Unlock Requirement"

    option_clear_half_in_act = 0
    option_b_rank_all = 1
    option_a_rank_all = 2
    option_perfect_all = 3
    default = 0


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


# endregion


class RhythmDoctorDeathLink(DeathLink):
    """
    When you die (a patient's heart breaks), everyone dies. The reverse is also true.
    """


# endregion
# endregion


@dataclass
class RhythmDoctorOptions(PerGameCommonOptions):
    # Generation options
    end_goal: EndGoal
    boss_unlock_requirement: BossUnlockRequirement
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
    powerup_chance: PowerupChance
    enable_easy_difficulty_powerups: EnableEasyDifficultyPowerups
    enable_strong_heart_powerups: EnableStrongHeartPowerups
    enable_ice_speed_powerups: EnableIceSpeedPowerups
    death_link: RhythmDoctorDeathLink


groups: list[OptionGroup] = [
    OptionGroup(
        "Generation Options",
        [
            EndGoal,
            BossUnlockRequirement,
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
        ],
    ),
    OptionGroup(
        "Powerup Options",
        [
            PowerupChance,
            EnableEasyDifficultyPowerups,
            EnableStrongHeartPowerups,
            EnableIceSpeedPowerups,
        ],
    ),
]

presets = {
    "Traps & Powerups": {
        "end_goal": EndGoal.option_helping_hands,
        "boss_unlock_requirement": BossUnlockRequirement.default,
        "perfect_ranks_excluded": True,
        "trap_chance": 33,
        "enable_fragile_heart_traps": True,
        "enable_character_scramble_traps": True,
        "enable_beatsound_scramble_traps": True,
        "enable_hitsound_scramble_traps": True,
        "enable_hard_difficulty_traps": True,
        "enable_chilli_speed_traps": True,
        "powerup_chance": 33,
        "enable_easy_difficulty_powerups": True,
        "enable_strong_heart_powerups": True,
        "enable_ice_speed_powerups": True,
        "death_link": False,
    },
}
