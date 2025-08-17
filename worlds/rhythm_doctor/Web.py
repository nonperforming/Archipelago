from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .Options import presets, groups

class RhythmDoctorWeb(WebWorld):
    rich_text_options_doc = True
    theme = "partyTime"
    bug_report_page = "https://github.com/nonperforming/RhythmDoctor.Archipelago/issues"

    # TODO: Where to put game page?
    # Other worlds only have setup here
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide for setting up Rhythm Doctor for Archipelago.",
        "English",
        "setup_en_US.md",
        "setup/en_US",
        [""]  # TODO: Fill this in with whoever writes the doc
    )]

    options_presets = presets
    option_groups = groups
