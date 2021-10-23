from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import requests

from bookmarker.links_md_parser import parse
from bookmarker.model import Bookmark, Note, ToRead


class Bookmarks:
    singleton = None
    path = Path.home() / "temp" / "links.md"

    def __init__(self):
        self.bookmarks = {}

    def add(self, bookmark):
        bookmark.id = str(len(self.bookmarks) + 1)
        self.bookmarks[bookmark.id] = bookmark
        with open(Bookmarks.path, "at") as f:
            print("\n---\n", file=f)
            print(f"## [{bookmark.title}]({bookmark.url})", file=f)
            urg = int(bookmark.to_read.is_urgent)
            imp = int(bookmark.to_read.is_important)
            print(f"\ntoread-urgent({urg})-important({imp})", file=f)
            print("\n### Notes", file=f)
            for note in bookmark.notes:
                print(f"\n#### {note.created_at.strftime('%Y-%m-%d')}", file=f)
                print(note.contents, file=f)
        return bookmark

    @classmethod
    def load(cls):
        if cls.singleton is None:
            cls.singleton = cls()
            with open(cls.path) as f:
                bookmarks = parse(f)
                for bookmark in bookmarks:
                    cls.singleton.bookmarks[bookmark.id] = bookmark
        return cls.singleton


def bookmarks():
    return list(Bookmarks.load().bookmarks.values())


def bookmark(id):
    return Bookmarks.load().bookmarks[id]


def add_bookmark(url, title=None, is_important=False, is_urgent=False, notes=""):
    # gdocs hack
    flds = urlsplit(url)
    if flds.netloc == "docs.google.com":
        path = flds.path.replace("/edit", "/")
        url = urlunsplit((flds.scheme, flds.netloc, path, "", ""))

    resp = requests.get(url)
    resp.raise_for_status()
    bookmark = Bookmark(
        url=url.strip(),
        title=title if title else "Placeholder Title",
        to_read=ToRead(is_important=is_important, is_urgent=is_urgent,),
        notes=[Note(created_at=datetime.now(), contents=notes)],
    )
    return Bookmarks.load().add(bookmark)
