// @flow
import "./bulma.min.css";
import "./custom.css";
import React from "react";
import { useState, useEffect } from "react";
import type {Node} from "react"
import {
  BrowserRouter as Router,
  Route,
  Switch,
  Link
} from "react-router-dom";
import { Navigation } from "./Navigation";
import { List } from "./List";
import { Show } from "./Show";
import { Edit } from "./Edit";
import { Add } from "./Add";

function App(): Node {
  const [bookmarks, setBookmarks] = useState(new Map());
  const [currentQuery, setCurrentQuery] = useState("");

  useEffect(() => {
    console.log("Loading all bookmarks");
    const allBookmarks = require("./bookmarks.json");
    let hsh = new Map();
    allBookmarks.forEach((bookmark) => hsh.set(bookmark.id, bookmark));
    setBookmarks(hsh);
  }, [1]);

  function editBookmark(updatedBookmark) {
    console.log("Inside editBoomark");
    if (bookmarks.has(updatedBookmark.id)) {
      let bookmarksCopy = new Map(bookmarks);
      let bookmark = bookmarksCopy.get(updatedBookmark.id);
      if (bookmark != null) {
        bookmark.title = updatedBookmark.title;
        bookmark.url = updatedBookmark.url;
        bookmark.notes = updatedBookmark.notes;
        setBookmarks(bookmarksCopy);
      }
    }
  }

  function deleteBookmark(bookmarkId) {
    console.log("Inside deleteBookmark");
    if (bookmarks.has(bookmarkId)) {
      let bookmarksCopy = new Map(bookmarks);
      bookmarksCopy.delete(bookmarkId);
      setBookmarks(bookmarksCopy);
    }
  }

  function addBookmark(newBookmark) {
    console.log("Inside addBookmark");
    let bookmarksCopy = new Map(bookmarks);
    let newId = Math.max(...[...bookmarks.keys()]) + 1;
    newBookmark.id = newId;
    bookmarksCopy.set(newId, newBookmark);
    setBookmarks(bookmarksCopy);
  }

  function searchBookmarks(query) {
    console.log("Inside searchBookmarks");
    let bookmarksCopy = new Map(bookmarks);
    bookmarksCopy.delete(1);
    bookmarksCopy.set(100, {
      id: 100,
      title: "The Twelve-Factor App",
      url: "https://12factor.net",
      notes: "This is a very cool philosophy on how to build web or even native apps. I think it applies to any microservice."
    })
    bookmarksCopy.set(101, {
      id: 101,
      title: "F# for fun and profit",
      url: "https://fsharpforfunandprofit.com",
      notes: "Some cool videos on functional programming taught with F#"
    });
    setCurrentQuery(query);
    setBookmarks(bookmarksCopy);
  }

  return (
    <Router>
      <Navigation />
      <Switch>
        <Route path="/list"><List bookmarks={bookmarks} searchBookmarks={searchBookmarks} currentQuery={currentQuery} /></Route>
        <Route path="/show/:id"><Show bookmarks={bookmarks} deleteBookmark={deleteBookmark} /></Route>
        <Route path="/edit/:id"><Edit bookmarks={bookmarks} editBookmark={editBookmark} /></Route>
        <Route path="/add"><Add addBookmark={addBookmark} /></Route>
        <Route path="/"><List bookmarks={bookmarks} searchBookmarks={searchBookmarks} currentQuery={currentQuery} /></Route>
      </Switch>
    </Router>
  );
}

export default App;