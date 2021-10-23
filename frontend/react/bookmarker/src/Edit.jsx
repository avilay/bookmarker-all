// @flow

import React from "react";
import type { Node } from "react";
import { useParams, useHistory } from "react-router-dom";
import { useState } from "react";

type Bookmark = {
  id: number,
  title: string,
  url: string,
  notes: string,
};

type Props = {
  bookmarks: Map<number, Bookmark>,
  editBookmark(Bookmark): void
};

function Edit(props: Props): Node {
  let { id } = useParams();  // have to use this variable name otherwise useParams does not work
  const bookmarkId = parseInt(id);
  const bookmark = props.bookmarks.get(bookmarkId);

  const [title, setTitle] = useState(bookmark?.title);
  const [url, setUrl] = useState(bookmark?.url);
  const [notes, setNotes] = useState(bookmark?.notes);
  let history = useHistory();

  if (bookmark == null) {
    return (<h3>This bookmark does not exist!</h3>);
  }

  function cancelClick(e) {
    e.preventDefault();
    history.goBack();
  }

  function saveClick(e) {
    e.preventDefault();
    console.log("Saving edits");
    props.editBookmark({
      id: bookmarkId,
      title: ((title: any): string),
      url: ((url: any): string),
      notes: ((notes: any): string)
    })
    history.goBack();
  }

  return (
    <section className="section">
      <div className="container">
        <div className="columns">
          <div className="column is-two-thirds">
            <h1 className="title">Edit Bookmark</h1>

            <div className="block">
              <div className="field">
                <label className="label">Title</label>
                <div className="control">
                  <input className="input" type="text" value={title} onChange={(e) => setTitle(e.target.value)} />
                </div>
              </div>
            </div>

            <div className="block">
              <div className="field">
                <label className="label">Url</label>
                <div className="control">
                  <input className="input" type="text" value={url} onChange={(e) => setUrl(e.target.value)} />
                </div>
              </div>
            </div>

            <div className="block">
              <div className="field">
                <label className="label">Notes</label>
                <div className="control">
                  <textarea className="textarea" value={notes} onChange={(e) => setNotes(e.target.value)} />
                </div>
              </div>
            </div>

            <div className="block">
              <div className="buttons">
                <button className="button is-info" onClick={saveClick}>Save</button>
                <button className="button" onClick={cancelClick}>Cancel</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export { Edit };