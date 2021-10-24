from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import requests

from .links_md_parser import parse
from .model import Bookmark, Note, ToRead

VERSION = "0.0.1"


class Bookmarks:
    singleton = None
    path = Path.home() / "temp" / "temp_links.md"

    def __init__(self):
        self.bookmarks = {}

    def _write_md(self, f, bookmark):
        print(f"## [{bookmark.title}]({bookmark.url})", file=f)
        if bookmark.to_read is not None:
            urg = int(bookmark.to_read.is_urgent)
            imp = int(bookmark.to_read.is_important)
            print(f"\ntoread-urgent({urg})-important({imp})", file=f)
        print("\n### Notes", file=f)
        for note in bookmark.notes:
            print(f"\n#### {note.created_at.strftime('%Y-%m-%d')}", file=f)
            print(note.contents.strip(), file=f)
        print("\n---\n", file=f)

    def update(self, bookmark):
        self.bookmarks[bookmark.id] = bookmark

    def save(self):
        Bookmarks.path.rename(Bookmarks.path.with_suffix(".prev.md"))
        with open(Bookmarks.path, "wt") as f:
            for bm in self.bookmarks.values():
                self._write_md(f, bm)

    def add(self, bookmark):
        bookmark.id = len(self.bookmarks) + 1
        self.bookmarks[bookmark.id] = bookmark
        with open(Bookmarks.path, "at") as f:
            self._write_md(f, bookmark)
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


def _standardize_url(url):
    # gdocs hack
    flds = urlsplit(url)
    if flds.netloc == "docs.google.com":
        path = flds.path.replace("/edit", "/")
        url = urlunsplit((flds.scheme, flds.netloc, path, "", ""))
    return url


def add_bookmark(url, title=None, to_read=None, notes=""):
    if bookmark_url(url):
        raise ValueError("Bookmark already exists!")
    url = _standardize_url(url)
    resp = requests.get(url)
    resp.raise_for_status()
    if to_read is None:
        tr = None
    else:
        tr = ToRead(
            is_important=to_read["is_important"], is_urgent=to_read["is_urgent"]
        )
    bookmark = Bookmark(
        url=url.strip(),
        title=title if title else "Placeholder Title",
        to_read=tr,
        notes=[Note(created_at=datetime.now(), contents=notes)],
    )
    return Bookmarks.load().add(bookmark)


def bookmark_url(url):
    url = _standardize_url(url)
    all_bookmarks = bookmarks()
    for bookmark in all_bookmarks:
        if bookmark.url == url:
            return bookmark
    return None


def set_to_read(id, to_read):
    bm = bookmark(id)
    if to_read is not None:
        bm.to_read = ToRead(
            is_important=to_read["is_important"], is_urgent=to_read["is_urgent"]
        )
    else:
        bm.to_read = None
    Bookmarks.load().update(bm)
    return bm


def add_notes(id, notes):
    bm = bookmark(id)
    bm.notes.append(Note(created_at=datetime.now(), contents=notes))
    Bookmarks.load().update(bm)
    return bm


def save():
    Bookmarks.load().save()
