import re
from datetime import datetime
from enum import Enum, auto
from functools import lru_cache

from .model import Bookmark, Note, ToRead


class State(Enum):
    EMPTY = auto()
    BOOKMARK = auto()
    NOTES = auto()
    NOTE = auto()


@lru_cache
def parse_link_header(line):
    return re.search(r"##\s*\[(.*)\]\((.*)\)", line)


def is_link_header(line):
    return parse_link_header(line) is not None


def extract_link_header(line):
    match = parse_link_header(line)
    return match.group(1), match.group(2)


@lru_cache
def parse_to_read(line):
    return re.search(r"toread\-urgent\((\d)\)\-important\((\d)\)", line)


def is_to_read(line):
    return parse_to_read(line) is not None


def extract_to_read(line):
    match = parse_to_read(line)
    is_urgent, is_important = match.group(1), match.group(2)
    return bool(int(is_urgent)), bool(int(is_important))


def is_notes_start(line):
    return line.startswith("### Notes")


@lru_cache
def parse_note_start(line):
    if line.startswith("####"):
        return re.search(r"(\d\d\d\d)\-(\d\d)\-(\d\d)", line)
    else:
        return None


def is_note_start(line):
    return parse_note_start(line) is not None


def extract_note_start(line):
    match = parse_note_start(line)
    return datetime(
        year=int(match.group(1)), month=int(match.group(2)), day=int(match.group(3))
    )


def is_end(line):
    return line.startswith("---")


def parse(file):
    bm = None
    note = None
    curr_state = State.EMPTY
    bookmarks = []
    for line in file:
        line = line.strip()
        if curr_state == State.EMPTY:
            # ignore everything unless it is a H2 with a title and a link
            if is_link_header(line):
                curr_state = State.BOOKMARK
                bm = Bookmark(id=len(bookmarks) + 1)
                bm.title, bm.url = extract_link_header(line)
                # bm.to_read = ToRead()
                bm.notes = []
        elif curr_state == State.BOOKMARK:
            # ignore everything unless it is toread or the beginning of Notes
            if is_to_read(line):
                bm.to_read = ToRead()
                bm.to_read.is_urgent, bm.to_read.is_important = extract_to_read(line)
            if is_notes_start(line):
                curr_state = State.NOTES
        elif curr_state == State.NOTES:
            # ignore everything unless it is the beginning of a note
            if is_note_start(line):
                created_at = extract_note_start(line)
                note = Note(created_at=created_at, contents="")
                curr_state = State.NOTE
        elif curr_state == State.NOTE:
            if is_end(line):
                bm.notes.append(note)
                curr_state = State.EMPTY
                bookmarks.append(bm)
                note = None
                bm = None
            elif is_note_start(line):
                bm.notes.append(note)
                created_at = extract_note_start(line)
                note = Note(created_at=created_at, contents="")
            else:
                # note.contents.append(line)
                note.contents += "\n" + line

    return bookmarks
