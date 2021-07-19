# -*- coding: utf-8 -*-

# Copyright (C) 2021 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import catapult
import subprocess

from catapult.i18n import _

ACTIONS = [{
    "desktops": ["GNOME"],
    "titles":   [_("Lock Screen")],
    "command":  "gnome-screensaver-command --lock",
}, {
    "desktops": ["GNOME"],
    "titles":   [_("Log Out"), _("Log Off")],
    "command":  "gnome-session-quit --logout",
}, {
    "desktops": ["GNOME"],
    "titles":   [_("Power Off"), _("Shutdown")],
    "command":  "gnome-session-quit --power-off",
}, {
    "desktops": ["GNOME"],
    "titles":   [_("Reboot"), _("Restart")],
    "command":  "gnome-session-quit --reboot",
}]


class SessionPlugin(catapult.Plugin):

    title = _("Session")

    def launch(self, window, id):
        self.debug(f"Launching {id}")
        subprocess.run(id, shell=True)

    def search(self, query):
        query = query.lower().strip()
        desktop = catapult.util.get_desktop_environment()
        for action in ACTIONS:
            if desktop not in action["desktops"]: continue
            offsets = [x.lower().find(query) for x in action["titles"]]
            offsets = [x for x in offsets if x >= 0]
            if not offsets: continue
            title = action["titles"][0]
            self.debug(f"Found {title} for {query!r}")
            yield catapult.SearchResult(
                description=action["command"],
                fuzzy=False,
                icon="application-x-executable",
                id=action["command"],
                offset=min(offsets),
                plugin=self,
                score=1,
                title=title,
            )
