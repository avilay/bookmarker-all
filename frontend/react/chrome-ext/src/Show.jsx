// @flow
import React from "react";
import type { Node } from "react";

type Note = {
  contents: string,
  createdAt: string
}

type ToRead = {
  isImportant: boolean,
  isUrgent: boolean
}

type Bookmark = {
  id: number,
  title: string,
  url: string,
  notes: Array<Note>,
  // toRead: ToRead
}

type Props = {
  bookmark: Bookmark
}

function Show(props: Props): Node {
  const bookmark = props.bookmark;

  return (
    <section clasName="section">
      <div className="container">
        <h1 className="subtitle is-3">{bookmark.title}</h1>

        <div className="block">
          <a href={bookmark.url}>{bookmark.url}</a>
        </div>

        <p className="block">
          Notes here...
        </p>

        <button className="button">Edit</button>

      </div>
    </section>
  );

}

export { Show };