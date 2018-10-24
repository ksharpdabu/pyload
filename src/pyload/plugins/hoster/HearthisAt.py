# -*- coding: utf-8 -*-
import json
import re


from ..internal.hoster import Hoster


class HearthisAt(Hoster):
    __name__ = "HearthisAt"
    __type__ = "hoster"
    __version__ = "0.03"
    __status__ = "testing"

    __pyload_version__ = "0.5"

    __pattern__ = r"https?://(?:www\.)?hearthis\.at/.*#pyload$"
    __config__ = [("enabled", "bool", "Activated", True)]

    __description__ = """Hearthis.at hoster plugin"""
    __license__ = "GPLv3"
    __authors__ = [("GammaC0de", "nitzo2001{AT]yahoo{DOT]com")]

    def setup(self):
        self.multiDL = True

    def process(self, pyfile):
        self.data = self.load(pyfile.url)

        m = re.search(r"intTrackId = (\d+);", self.data)
        if m is None:
            self.fail(self._("Track ID not found"))

        track_id = m.group(1)

        data = self.load(
            "https://hearthis.at/playlist.php", post={"tracks[]": track_id}
        )
        json_data = json.loads(data)

        pyfile.name = json_data[0]["title"] + ".mp3"

        self.download(json_data[0]["track_url"])