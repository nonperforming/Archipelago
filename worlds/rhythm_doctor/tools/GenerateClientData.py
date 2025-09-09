from typing import TYPE_CHECKING

from worlds.rhythm_doctor import GAME
from worlds.rhythm_doctor.Data import all_regular_stages, all_boss_stages, \
    act_3_boss, act_3_secret_boss, \
    FILLER_TRAPS, FILLER_POWERUPS, REGIONS

if TYPE_CHECKING:
    from worlds.rhythm_doctor import RhythmDoctorWorld

short_to_internal_name = {
    # region Act 1 - Main Ward
    "1-1": "Level.OrientalTechno",
    "1-1N": "Level.OrientalDubstep",
    "1-2": "Level.Intimate",
    "1-2N": "Level.IntimateH",  # Intimate (Night)
    "1-X": "Level.OrientalInsomniac",
    "1-CNY": "Level.GongXi",  # Chinese New Year
    "1-BOO": "Level.Halloween",  # Theme Of Really Spooky Bird
    # endregion

    # region Act 2 - SVT Ward
    "2-1": "Level.Lofi",  # Lofi Hip Hop Beats To Treat Patients To
    "2-1N": "Level.CareLess",  # Wish I Could Care Less
    "2-2": "Level.SVT",  # Supraventricular Tachycardia
    "2-2N": "Level.Unreachable",
    "2-3": "Level.Smokin",  # Puff Piece
    "2-3N": "Level.Pomeranian",  # Bomb Sniffing Pomeranian
    "2-4": "Level.SongOfTheSea",
    "2-4N": "Level.SongOfTheSeaH",  # Song of the Sea (Night)
    "2-X": "Level.Boss2",  # All The Times
    "2-B1": "Level.BeansHopper",
    # endregion

    # region Act 3 - Main Ward
    "3-1": "Level.Garden",  # Sleepy Garden
    "3-1N": "Level.Lounge",
    "3-2": "Level.Classy",  # Classy
    "3-2N": "Level.ClassyH",  # Classy (Night)
    "3-3": "Level.DistantDuet",
    "3-3N": "Level.DistantDuetH",  # Distant Duet (Night)
    "3-X": "Level.Lesmis",  # One Shift More
    "3-DOG": "Level.Lesmis",  # "Rhythm Dogtor" - not official name
    # endregion

    # region Act 4 - Train
    "4-1": "Level.Heldbeats",  # Training Doctor's Train Ride Performance
    "4-1N": "Level.Rollerdisco",  # Rollerdisco Rumble
    "4-2": "Level.Invisible",
    "4-2N": "Level.InvisibleH",  # Invisible (Night)
    "4-3": "Level.Steinway",
    "4-3N": "Level.SteinwayH",  # Steinway Reprise
    "4-4": "Level.KnowYou",
    "4-4N": "Level.Murmurs",
    "1-XN": "Level.InsomniacHard",  # Super Battleworn Insomniac
    # endregion

    # region Act 5 - Physiotherapy Ward
    "5-1": "Level.LuckyBreak",
    "5-1N": "Level.Injury",  # One Slip Too Late
    "5-2": "Level.Freezeshot",  # Lofi Beats For Patients To Chill To
    "5-2N": "Level.FreezeshotH",  # Unsustainable Inconsolable
    "5-3": "Level.AthleteTherapy",  # Seventh Inning Stretch
    "5-B1": "Level.RhythmWeightlifter",
    "5-X": "Level.AthleteFinale",  # Dreams Don't Stop
    # endregion

    # region Bonus - Basement
    "X-FTS": "Level.VividStasis",  # vivid/stasis - Fixations Toward the Stars
    "X-KOB": "Level.SparkLine",  # Circle of Sparks - Kingdom of Balloons
    "X-WOT": "Level.Unbeatable",  # UNBEATABLE - Worn Out Tapes
    "X-MAT": "Level.MeetAndTweet",  # Bits & Bops - Meet and Tweet
    # region Muse Dash
    "MD-1": "Level.BlackestLuxuryCar",
    "MD-2": "Level.TapeStopNight",
    "MD-3": "Level.The90sDecision",
    # endregion
    "X-1": "Level.ArtExercise",
    # endregion

    # region Art Room
    "X-0": "Level.HelpingHands",
    # endregion
}


def build_internal_name_to_stage(world: "RhythmDoctorWorld") -> str:
    buffer = "/// <summary>\n" + \
             """/// <see cref="Level"/> to corresponding <see cref="LevelBase"/>\n""" + \
             "/// </summary>\n" + \
             """/// <seeAlso cref="RegularStage"/>\n""" + \
             """/// <seeAlso cref="BossStage"/>\n""" + \
             "internal static readonly Dictionary<Level, BaseStage> LevelToStage = new() {"

    for regular_stage in all_regular_stages:
        constructor = ""
        if regular_stage.act is None:
            constructor += "Act.None, "
        else:
            constructor += f"Act.{regular_stage.act.replace(" ", "")}, "

        if regular_stage.b_rank_location:
            constructor += str(world.location_name_to_id[f"{regular_stage.name} - B Rank"])
        else:
            constructor += "null"
        constructor += ", "
        if regular_stage.a_rank_location:
            constructor += str(world.location_name_to_id[f"{regular_stage.name} - A Rank"])
        else:
            constructor += "null"
        constructor += ", "
        if regular_stage.s_rank_location:
            constructor += str(world.location_name_to_id[f"{regular_stage.name} - S Rank"])
        else:
            constructor += "null"

        buffer += f"\n  {{ {short_to_internal_name[regular_stage.short_name]}, new RegularStage({constructor}) }},"

    # We exclude 3-X and 3-DOG here as they are a special case - they are handled separately afterward
    for boss_stage in [boss_stage for boss_stage in all_boss_stages
                       if not (boss_stage.short_name == act_3_boss.short_name
                               or boss_stage.short_name == act_3_secret_boss.short_name)]:
        constructor = f"Act.{boss_stage.act.replace(" ", "")}, "
        if boss_stage.clear_location:
            constructor += str(world.location_name_to_id[f"{boss_stage.name} - Clear"])
        else:
            constructor += "null"
        constructor += ", "
        if boss_stage.clear_plus_location:
            constructor += str(world.location_name_to_id[f"{boss_stage.name} - Complete+ Without Checkpoints"])
        else:
            constructor += "null"
        constructor += ", "
        if boss_stage.clear_perfect_location:
            constructor += str(world.location_name_to_id[f"{boss_stage.name} - Perfect Clear"])
        else:
            constructor += "null"

        buffer += f"\n  {{ {short_to_internal_name[boss_stage.short_name]}, new BossStage({constructor}) }},"

    # Handle special 3-X/3-DOG case
    lesmis_constructor = ("Act.Act3, "
                          f"{world.location_name_to_id[f"{act_3_boss.name} - Clear"]}, "
                          f"null, "
                          f"{world.location_name_to_id[f"{act_3_boss.name} - Perfect Clear"]}")
    buffer += (f"\n  {{ Level.Lesmis, new BossStage({lesmis_constructor}, "
               f"new Dictionary<string, long> "
               f"{{ {{ \"dog_clear\", {world.location_name_to_id[f"{act_3_secret_boss.name} - Clear"]} }}, "
               f"{{ \"dog_perfect\", {world.location_name_to_id[f"{act_3_secret_boss.name} - Perfect Clear"]} }} "
               f"}}) }},")

    buffer += "\n};\n\n"
    return buffer


def build_item_id_to_level(world: "RhythmDoctorWorld") -> str:
    buffer = "/// <summary>\n" + \
             """/// Level ID to corresponding <see cref="Level"/>\n""" + \
             "/// </summary>\n" + \
             "internal static readonly Dictionary<long, Level> ItemIdToLevel = new() {"

    for stage in all_regular_stages:
        buffer += f"""\n  {{ {world.item_name_to_id[stage.name]}, {short_to_internal_name[stage.short_name]} }},"""

    buffer += "\n};\n\n"
    return buffer


def build_item_id_to_trap(world: "RhythmDoctorWorld") -> str:
    buffer = "/// <summary>\n" + \
             "/// Trap item ID to corresponding <see cref=\"Level\"/>\n" + \
             "/// </summary>\n" + \
             "internal static readonly Dictionary<long, Type> TrapItemIdToLevel =\n" + \
             "  new()\n" + \
             "  {\n"

    # Requires someone to go in and fill in the types manually
    for trap in FILLER_TRAPS + FILLER_POWERUPS:
        buffer += f"  {{ {world.item_name_to_id[trap]}, typeof({trap}) }},\n"

    buffer += "\n};\n\n"

    return buffer


def build_key_item_id_to_ward(world: "RhythmDoctorWorld") -> str:
    buffer = "/// <summary>\n" + \
             "/// Key item ID to corresponding <see cref=\"Region\"/>\n" + \
             "/// </summary>\n" + \
             "internal static readonly Dictionary<long, Region> KeyItemIdToWard =\n" + \
             "  new()\n" + \
             "  {\n"

    for ward in REGIONS:
        if ward == "Main Ward":
            continue

        # Requires manual fixing
        buffer += f"  {{ {world.item_name_to_id[f"{ward} Key"]}, Region.{ward.replace(" ", "")} }},\n"

    buffer += "\n};\n\n"

    return buffer

def main(world: "RhythmDoctorWorld"):
    """
    Generate client data used by the C# client.
    Call after set_rules().
    """
    file = "#region Generated by APWorld\n"
    file += f"""internal const string GAME = "{GAME}";\n"""
    file += f"""internal const long SLEEVE_PAINT_ITEM_ID = {world.item_name_to_id["Sleeve Paint"]};\n"""
    file += build_internal_name_to_stage(world)
    file += build_item_id_to_level(world)
    file += build_item_id_to_trap(world)
    file += build_key_item_id_to_ward(world)
    file += "#endregion"

    with open("RhythmDoctorBindings.cs", "w") as file_stream:
        file_stream.write(file)
