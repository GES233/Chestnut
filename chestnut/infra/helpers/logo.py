""" `chestnut.infra.helpers.logo`

    Logo in ASCII art.
"""
from typing import Any, Tuple


CHESTNUT_ICON_SMALL = """🌰 with 🥥, 🍩 and 🍈"""


CHESTNUT_ICON_MIDIAN = """
╔═╗┬ ┬┌─┐┌─┐┌┬┐┌┐┌┬ ┬┌┬┐
║  ├─┤├┤ └─┐ │ ││││ │ │ 
╚═╝┴ ┴└─┘└─┘ ┴ ┘└┘└─┘ ┴ 
"""


CHESTNUT_ICON_LARGE = """
"""


ICON_NAIVE = """
   ▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄   
   █      █▄▄█      █   
   █▄▄▄▄▄▄█  █▄▄▄▄▄▄█   
          ▄  ▄          
                        
 keep simple, keep naive
"""
"+1s"


def sizecalc(logo: str) -> Tuple[int, int]:
    """Return the size of ascii art ilustration as (raw, column)."""

    lines = logo.split("\n")

    column = 0
    for line in lines:
        if len(line) > column:
            column = len(line)

    raw = len(lines)

    return raw, column
