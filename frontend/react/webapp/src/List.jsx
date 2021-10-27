// @flow

import React from "react";
import { useState } from "react";
import type {Node} from "react";
import { Link } from "react-router-dom";

type Bookmark = {
  id: number,
  title: string,
  url: string,
  notes: string,
};

type Props = {
  currentQuery: string,
  bookmarks: Map<number, Bookmark>,
  searchBookmarks(string): void
};

function List(props: Props): Node {
  const [searchQuery, setSearchQuery] = useState(props.currentQuery);

  function searchClick(e) {
    e.preventDefault();
    console.log("inside searchClick");
    props.searchBookmarks(searchQuery);
  }

  const bookmarks = [...props.bookmarks.values()].map((bookmark) => {
    return (
      <article key={bookmark.id.toString()} className="block">
        <Link to={`/show/${bookmark.id}`}>{bookmark.title}</Link>
      </article>
    );
  });

  return (
    <section className="section">
      <div className="container">
        {/* header */}
        <div className="level">
          <div className="level-left">
            {/** title */}
            <div className="level-item">
              <h1 className="title">Bookmarks</h1>
            </div>
            {/** end title */}

            {/** search box */}
            <div className="level-item">
              <div className="field has-addons">
                <p className="control">
                  <input
                    className="input"
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)} />
                </p>
                <p className="control">
                  <button className="button is-info is-light is-outlined" onClick={searchClick}>Search</button>
                </p>
              </div>
            </div>
            {/** end search box */}
          </div>
        </div>
        {/* end header */}

        {bookmarks}
      </div>
    </section>
  );
}

export {List};
