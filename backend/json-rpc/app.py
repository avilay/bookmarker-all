import traceback
from dataclasses import asdict
from functools import partial

import bmservice as svc
import werkzeug.exceptions as ex
from flask import Flask, abort, request
from flask_cors import CORS
from inflection import camelize, underscore

import time

app = Flask(__name__)
CORS(app)


def fix_naming(obj, convert):
    if isinstance(obj, dict):
        new_obj = {}
        for key, val in obj.items():
            new_obj[convert(key)] = fix_naming(val, convert)
        return new_obj
    elif isinstance(obj, list):
        new_obj = []
        for elem in obj:
            new_obj.append(fix_naming(elem, convert))
        return new_obj
    else:
        return obj


@app.errorhandler(ex.NotFound)
def handle_not_found(e):
    app.logger.error(f"NotFound error: {e.description}")
    return {"code": -32601, "message": e.description}, e.code


@app.errorhandler(ex.BadRequest)
def handle_bad_request(e):
    app.logger.error(f"BadReqeust error: {e.description}")
    return {"code": -32700, "message": e.description}, e.code


@app.errorhandler(TypeError)
def handle_type_error(e):
    app.logger.error(f"TypeError: {str(e)}")
    traceback.print_exc()
    return {"code": -32600, "message": str(e)}, 400


@app.errorhandler(ValueError)
def handle_value_error(e):
    app.logger.error(f"ValueError: {str(e)}")
    return {"code": -32602, "message": str(e)}, 400


@app.route("/", methods=["POST"])
def endpoint():
    print(request.data.decode("utf-8"))
    print("is json: ", request.is_json)
    req = request.get_json()
    if "jsonrpc" not in req or req["jsonrpc"] != "2.0":
        raise TypeError("jsonrpc property absent or not set to 2.0")
    if "id" not in req:
        raise TypeError("Request object is missing an id.")
    if "method" not in req:
        raise TypeError("Request object is missing a method.")

    method_name = underscore(req["method"])
    func = globals().get(method_name, None)
    if not func:
        abort(404, f"Method {req['method']} not found.")

    params = req.get("params", None)
    if params:
        if isinstance(params, list):
            result = func(*fix_naming(params, underscore))
        elif isinstance(params, dict):
            result = func(**fix_naming(params, underscore))
        else:
            abort(400, "Something wrong with params.")
    else:
        result = func()

    return {"jsonrpc": "2.0", "id": req["id"], "result": result}


def get_bookmark_by_id(bookmark_id):
    js_naming = partial(camelize, uppercase_first_letter=False)
    try:
        bm = svc.bookmark(bookmark_id)
        return fix_naming(asdict(bm), js_naming)
    except KeyError:
        raise ValueError(f"Bookmark id {bookmark_id} does not exist.")


def get_all_bookmarks():
    bookmarks = [asdict(bookmark) for bookmark in svc.bookmarks()]
    js_naming = partial(camelize, uppercase_first_letter=False)
    return fix_naming(bookmarks, js_naming)


def get_bookmark_by_url(url):
    bm = svc.bookmark_url(url)
    if bm is None:
        print("Got None")
        time.sleep(2)
        return ""
    else:
        print(bm)
        js_naming = partial(camelize, uppercase_first_letter=False)
        return fix_naming(asdict(bm), js_naming)


def new_bookmark(url, notes, title, to_read=None):
    js_naming = partial(camelize, uppercase_first_letter=False)
    bm = svc.add_bookmark(url, title, to_read, notes)
    return fix_naming(asdict(bm), js_naming)


def update_bookmark(
    bookmark_id, mark_as_read=None, is_important=None, is_urgent=None, notes=None
):
    if (
        mark_as_read is None
        and is_urgent is None
        and is_important is None
        and notes is None
    ):
        raise ValueError("All update fields cannot be null.")
    if (is_urgent is not None and is_important is None) or (
        is_urgent is None and is_important is not None
    ):
        raise ValueError("Either both isImportant and isUrgent must be set or neither.")
    if mark_as_read is not None and (is_important is not None or is_urgent is not None):
        raise ValueError(
            "Cannot set both markAsRead and one of isImportant or isUrgent."
        )

    if notes is not None:
        bm = svc.add_notes(bookmark_id, notes)
    if mark_as_read is not None:
        bm = svc.set_to_read(bookmark_id, None)
    elif is_urgent is not None and is_urgent is not None:
        bm = svc.set_to_read(
            bookmark_id, {"is_urgent": is_urgent, "is_important": is_important}
        )
    svc.save()
    js_naming = partial(camelize, uppercase_first_letter=False)
    return fix_naming(asdict(bm), js_naming)
