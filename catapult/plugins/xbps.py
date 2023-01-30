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

import subprocess
import re

from catapult.api import Plugin
from catapult.api import SearchResult
from catapult.i18n import _


class XbpsPlugin(Plugin):

    title = _("xbps")

    def launch(self, window, id):
        self.debug(f"Launching {id}")
        #subprocess.Popen(["kitty","sudo", "xbps-install", id])
        subprocess.run(["kitty","--hold" , "--detach", "sudo", "-p", f"{id}\nPassword:"] + id.split(" ")[:3])
        
    def search(self, query):
        query = query.lower().strip()
        if not query.startswith("!"):
            return
        
        query = query[1:]
        args = ["xbps-query", "-Rs", f"""{query}"""] if query else ["xbps-query", "-m"]

        queryProcess = subprocess.Popen(args, stdout=subprocess.PIPE, universal_newlines=True)

        for line in queryProcess.stdout.readlines():
            app = re.split('\s+', line, 2)
            app = app if len(app) > 2 else ["[*]", app[0], app[0]]
            yield SearchResult(
                description=app[2],
                fuzzy=False,
                icon="folder-download-symbolic" if app[0] == "[-]" else "user-trash",
                id=f"xbps-install -S {app[1]} \n{app[2]}" if app[0] == "[-]" else f"xbps-remove -o {app[1]} \n{app[2]}",
                offset=0,
                plugin=self,
                score=1,
                title=app[1],
            )
