from dataclasses import dataclass
from Options import PerGameCommonOptions, DeathLink, StartInventoryPool, Choice, DefaultOnToggle, \
    Range, Toggle, OptionGroup
#from . import RhythmDoctorWorld

#def adjust_options(world: RhythmDoctorWorld):
#    pass

#region Options
#region Generation
class EndGoal(Choice):
    """
    The end goal required to beat the game.

    **X-0 - Helping Hands:**
    Clear all other bosses (1-X, 2-X, 3-X, 1-XN, 5-X) to unlock X-0 - Helping Hands.
    Then, clear X-0 to beat the game!

    **Clear All Levels:**
    Clear all levels with a B rank or higher to beat the game!

    **Perfect All Levels:**
    Clear all levels with an S+/Perfect rank to beat the game!
    """
    display_name = "End Goal"

    option_helping_hands = 0
    option_clear_all = 1
    option_perfect_all = 2
    default = 0


class BossUnlockRequirement(Choice):
    """
    The requirements to unlock the boss level for an act.

    **Half:**
    Only half the number of levels in the ward are required to be cleared with a B rank or higher to unlock the act's boss.

    **All:**
    All the number of levels in the ward are required to be cleared with a B rank or higher to unlock the act's boss.

    **Perfect:**
    All the number of levels in the ward are required to be cleared with a S+ rank or higher to unlock the act's boss.
    """
    auto_display_name = "Boss Unlock Requirement"

    option_half = 0
    option_all = 1
    option_perfect = 2
    default = 0


#endregion

#region Gameplay
#region Traps
class TrapChance(Range):
    """Determines the likeliness of a **filler item becoming a trap**."""
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 50


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


# TODO: This can get problematic with Hall of Mirrors
#class EnableScreenEffectTraps(DefaultOnToggle):
#    """Determines if **screen effect traps** should be in the item pool."""
#    display_name = "Enable Screen Effect Traps"

class EnableSpeedTraps(Toggle):
    """Determines if **🌶️ speed traps** should be in the item pool."""
    display_name = "Enable Speed Traps"


#endregion

#region Powerups
class EnableEasyDifficultyPowerups(Toggle):
    """Determines if **easy difficulty powerups** should be in the item pool."""
    display_name = "Enable Easy Difficulty Powerups"


class EnableStrongHeartPowerups(Toggle):
    """Determines if **decreased mistake weight powerups** should be in the item pool."""
    display_name = "Enable Strong Heart Powerups"


class EnableSlowPowerups(Toggle):
    """Determines if **🧊 slow powerups** should be in the item pool."""
    display_name = "Enable Slow Powerups"


#endregion
#endregion
#endregion

@dataclass
class RhythmDoctorOptions(PerGameCommonOptions):
    # FIXME: What? This seems to be a common variable set in a lot of Options
    # Should we include a random level from Act 1/Act 3 here?
    # Or instead use push_precollected in generate_early?
    # Generation options
    #start_inventory_from_pool: StartInventoryPool

    # Generation options
    end_goal: EndGoal
    boss_unlock_requirement: BossUnlockRequirement

    # Gameplay options
    trap_chance: TrapChance
    enable_fragile_heart_trap: EnableFragileHeartTraps
    enable_character_scramble_trap: EnableCharacterScrambleTraps
    enable_beatsound_scramble_trap: EnableBeatsoundScrambleTraps
    enable_hitsound_scramble_trap: EnableHitsoundScrambleTraps
    enable_hard_difficulty_trap: EnableHardDifficultyTraps
    #enable_screen_effect_trap: EnableScreenEffectTraps
    enable_speed_trap: EnableSpeedTraps
    enable_easy_difficulty_powerup: EnableEasyDifficultyPowerups
    enable_strong_heart_powerup: EnableStrongHeartPowerups
    enable_slow_powerup: EnableSlowPowerups
    death_link: DeathLink


groups: list[OptionGroup] = [
    OptionGroup("Generation Options", [
        EndGoal,
        BossUnlockRequirement,
    ]),
    OptionGroup("Gameplay Options", [
        DeathLink,
    ]),
    OptionGroup("Trap Options", [
        TrapChance,
        EnableFragileHeartTraps,
        EnableCharacterScrambleTraps,
        EnableBeatsoundScrambleTraps,
        EnableHitsoundScrambleTraps,
        EnableHardDifficultyTraps,
        #EnableScreenEffectTraps,
        EnableSpeedTraps,
    ]),
    OptionGroup("Powerup Options", [
        EnableEasyDifficultyPowerups,
        EnableStrongHeartPowerups,
        EnableSlowPowerups,
    ]),
]

presets = {
    "Default": {
        "end_goal": EndGoal.option_helping_hands,
        "boss_unlock_requirement": BossUnlockRequirement.default,
        "trap_chance": TrapChance.default,
        "enable_fragile_heart_trap": False,
        "enable_character_scramble_trap": False,
        "enable_beatsound_scramble_trap": False,
        "enable_hitsound_scramble_trap": False,
        "enable_hard_difficulty_trap": False,
        #"enable_screen_effect_trap": False,
        "enable_speed_trap": False,
        "enable_easy_difficulty_powerup": False,
        "enable_strong_heart_powerup": False,
        "enable_slow_powerup": False,
        "death_link": False,
    },
    "Traps & Powerups": {
        "end_goal": EndGoal.option_helping_hands,
        "boss_unlock_requirement": BossUnlockRequirement.default,
        "trap_chance": TrapChance.default,
        "enable_fragile_heart_trap": True,
        "enable_character_scramble_trap": True,
        "enable_beatsound_scramble_trap": True,
        "enable_hitsound_scramble_trap": True,
        "enable_hard_difficulty_trap": True,
        #"enable_screen_effect_trap": True,
        "enable_speed_trap": True,
        "enable_easy_difficulty_powerup": True,
        "enable_strong_heart_powerup": True,
        "enable_slow_powerup": True,
        "death_link": False,
    },
}
