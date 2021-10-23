from dataclasses import dataclass

from ariadne import (
    MutationType,
    ObjectType,
    QueryType,
    UnionType,
    convert_kwargs_to_snake_case,
    load_schema_from_path,
    make_executable_schema,
    resolve_to,
)
from ariadne.asgi import GraphQL

import bookmarker.data as data
from bookmarker.model import Bookmark, ToRead

query = QueryType()
bookmark = ObjectType("Bookmark")
note = ObjectType("Note")
to_read = ObjectType("ToRead")
bookmark_response = UnionType("BookmarkResponse")
mutation = MutationType()
add_bookmark_response = UnionType("AddBookmarkResponse")


@dataclass
class BookmarkNotFound:
    code: int
    message: str
    bad_bookmark_id: str


@dataclass
class InvalidUrl:
    code: str
    message: str
    bad_url: str


@query.field("bookmarks")
def resolve_bookmarks(*_):
    return data.bookmarks()


@query.field("bookmark")
def resolve_boomark(*_, id):
    try:
        return data.bookmark(id)
    except IndexError:
        return BookmarkNotFound(
            code=-1, message="Bookmark not in database", bad_bookmark_id=id
        )


@bookmark_response.type_resolver
def resolve_bookmark_response_type(obj, *_):
    return type(obj).__name__


resolve_to("id")(Bookmark, None)
resolve_to("url")(Bookmark, None)
resolve_to("title")(Bookmark, None)
resolve_to("notes")(Bookmark, None)
resolve_to("isImportant")(ToRead, None)
resolve_to("isUrgent")(ToRead, None)


@bookmark.field("toRead")
def resolve_to_read(bookmark, _):
    return bookmark.to_read


@to_read.field("isUrgent")
def resolve_is_urgent(tr, _):
    return tr.is_urgent


@to_read.field("isImportant")
def resolve_is_important(tr, _):
    return tr.is_important


@note.field("createdAt")
def resolve_created_at(note, _):
    return str(note.created_at)


@note.field("contents")
def resolve_contents(note, _):
    # return " ".join(note.contents)
    return note.contents


@mutation.field("addBookmark")
@convert_kwargs_to_snake_case
def resolve_add_bookmark(
    *_, url, title=None, is_important=False, is_urgent=False, notes=""
):
    return data.add_bookmark(url, title, is_important, is_urgent, notes)


@add_bookmark_response.type_resolver
def resolve_add_bookmark_response_type(obj, *_):
    return type(obj).__name__


def start():
    typedefs = load_schema_from_path("../bookmarker.graphql")
    schema = make_executable_schema(
        typedefs,
        query,
        bookmark,
        note,
        to_read,
        bookmark_response,
        mutation,
        add_bookmark_response,
    )
    return GraphQL(schema, debug=True)


app = start()
