// @flow
import React from "react";
import type { Node } from "react";
import { useParams, Link, useHistory } from "react-router-dom";
import { useState } from "react";

type Bookmark = {
  id: number,
  title: string,
  url: string,
  notes: string,
};

type Props = {
  bookmarks: Map<number, Bookmark>,
  deleteBookmark(number): void
};

function Show(props: Props): Node {
  let { id } = useParams();
  let history = useHistory();
  const [showDeleteConfirm, setShowDeleteConfirm] = useState("");

  let bookmarkId = parseInt(id);
  const bookmark = props.bookmarks.get(bookmarkId);
  if (bookmark == null) {
    return (
      <section className="section">
        <div className="container">
          <h1 className="subtitle is-3">This bookmark does not exist!</h1>
        </div>
      </section>
    );
  }

  function onDeleteClick(e) {
    e.preventDefault();
    props.deleteBookmark(bookmarkId);
    history.replace({pathname: "/list"});
  }

  return (
    <section className="section">
      <div className="container">
        <h1 className="subtitle is-3">{bookmark.title}</h1>

        <div className="block">
          <a href={bookmark.url}>{bookmark.url}</a>
        </div>

        <p className="block">
          {bookmark.notes}
        </p>


        <div className={`modal ${showDeleteConfirm}`}>
          <div className="modal-background"></div>
          <div className="modal-content">
            <div className="box">
              <div className="block">
                <p className="is-size-4">Are you sure?</p>
              </div>
              <div className="block">
                <div className="buttons">
                  <button className="button is-danger" onClick={onDeleteClick}>Yes, Delete!</button>
                  <button className="button" onClick={(e) => setShowDeleteConfirm("")}>No, Get me out of here!</button>
                </div>
              </div>
            </div>
          </div>
          <button className="modal-close is-large" aria-label="close" onClick={(e) => setShowDeleteConfirm("")}></button>
        </div>


        <div className="block">
          <div className="buttons">
            <Link className="button" to={`/edit/${bookmark.id}`}>Edit</Link>
            <button className="button is-danger" onClick={(e) => setShowDeleteConfirm("is-active")}>Delete</button>
          </div>
        </div>
      </div>
    </section>
  );
}

export { Show };