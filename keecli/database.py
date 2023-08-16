"""Database interface to the .kdbx file"""

import json
import re

import structlog
from pykeepass import PyKeePass
from pykeepass.entry import Entry
from pykeepass.group import Group

logger = structlog.get_logger()


def entry_to_dict(self, show_password: bool = False):
    return {
        "Group": self.group.name,
        "Name": self.title,
        "Username": self.username,
        "Password": self.password if show_password else re.sub(".", "*", self.password),
        "URL": self.url,
        "Notes": self.notes,
    }


def entry_to_json(self):
    return json.dumps(self.to_dict())


Entry.to_dict = entry_to_dict
Entry.to_json = entry_to_json


class KeePassDatabase:
    def __init__(self, filename: str, password: str):
        """Open the database file"""
        self._kp = PyKeePass(filename, password)

    def get_entry(self, name: str, group: str) -> Entry:
        if not group:
            return self._kp.find_entries_by_title(name, flags="i", regex=True)

        groups = self._kp.find_groups(name=group, regex=True, flags="i")
        return [
            self._kp.find_entries(title=name, group=group, regex=True, flags="i")
            for group in groups
        ]

    def get_entries(self, group: Group) -> list[Entry]:
        return sorted(group.entries, key=lambda entry: entry.title.lower())

    def get_groups(self) -> list[Group]:
        return sorted(
            [group for group in self._kp.groups], key=lambda group: group.name.lower()
        )
