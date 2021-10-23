// @flow
import "./bulma.min.css";
import "./custom.css";
import React from "react";
import type { Node } from "react"
import { Link } from "react-router-dom";


function Navigation(): Node {
  return (
    <nav className="navbar is-info" role="navigation" aria-label="main navigation">
      <div className="navbar-brand">
        <a className="navbar-item is-size-3 has-text-weight-semibold" href="/">Bookmarker</a>

        <a role="button" className="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div id="navbarBasicExample" className="navbar-menu">
        <div className="navbar-start">
          <Link className="navbar-item" to="/list">Bookmarks</Link>
          <a className="navbar-item">Collections</a>
          <div className="navbar-item has-dropdown is-hoverable">
            <a className="navbar-link">New</a>
            <div className="navbar-dropdown">
              <Link className="navbar-item" to="/add">Bookmark</Link>
              <a className="navbar-item">Collection</a>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

export { Navigation };