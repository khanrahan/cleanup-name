"""
Cleanup Name

URL:

    https://github.com/khanrahan/cleanup-name

Description:

    Cleanup selected clip names.  Remove all symbols and convert all spaces to
    underscores.

Menus:

    Right-click selected clips on a reel -> Edit... -> Cleanup Name
    Right-click selected clips in the Media Panel -> Edit... -> Cleanup Name

To Install:

    For all users, copy this file to:
    /opt/Autodesk/shared/python

    For a specific user, copy this file to:
    /opt/Autodesk/user/<user name>/python
"""

from __future__ import print_function

__title__ = "Cleanup Name"
__version_info__ = (0, 1, 0)
__version__ = ".".join([str(num) for num in __version_info__])
__version_title__ = "{} v{}".format(__title__, __version__)

MESSAGE_PREFIX = "[PYTHON HOOK]"


def message(string):
    """Print message to shell window and append global MESSAGE_PREFIX."""

    print(" ".join([MESSAGE_PREFIX, string]))


def cleanup_text(text):
    """Returns string that is appropriate for filename usage."""

    import re

    # Delete first and last character if a symbol or space.
    chopped = re.sub(r"^[\W_]+|[\W_]+$", "", text)
    # Convert symbols & whitespace to underscores.
    sanitized = re.sub(r"\W+", "_", chopped)
    # Remove duplicate underscores.
    tidy = re.sub(r"(_)\1+", "_", sanitized)

    return tidy


def cleanup_clip_name(selection):
    """Print output and loop through selected clips to cleanup their names."""

    message(__version_title__)
    message("Script called from {}".format(__file__))

    for clip in selection:
        name = clip.name.get_value()

        clean = cleanup_text(name)

        if clean == name:
            message("Skipping {}. No changes necessary.".format(name))
            continue

        clip.name.set_value(clean)
        message("Renamed {} to {}".format(name, clean))

    message("Done!")


def scope_clip(selection):

    import flame

    for item in selection:
        if isinstance(item, flame.PySequence):
            return True
    return False


def get_media_panel_custom_ui_actions():

    return [{'name': "Edit...",
             'actions': [{'name': "Cleanup Name",
                          'isVisible': scope_clip,
                          'execute': cleanup_clip_name,
                          'minimumVersion': "2020.3.1"}]
            }]
