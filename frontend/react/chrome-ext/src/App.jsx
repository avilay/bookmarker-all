// @flow
import "./bulma.min.css";
import "./custom.css";
import React from "react";
import type {Node} from "react";
import chrome from "./chrome";
import { useState, useEffect } from "react";
import { Show } from "./Show";


function App(): Node {
  const [result, setResult] = useState({
    isLoading: true,
    bookmark: {
      id: -1,
      title: "",
      url: "",
      notes: [],
      // toRead: {
      //   isImportant: false,
      //   isUrgent: false
      // }
    }
  });

  console.debug("Inside App isLoading: ", result.isLoading);

  useEffect(() => {
    console.debug("Running effect");

    chrome.runtime.sendMessage('get-url', (url) => {
      fetch("http://localhost:5000", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          jsonrpc: "2.0",
          id: 1,
          method: "getBookmarkByUrl",
          params: [url]
        })
      })
      .then((resp) => resp.json())
      .then((json) => {
        console.debug("Setting result.isLoading to false");
        let newBookmark = {
          id: json.result.id,
          title: json.result.title,
          url: json.result.url,
          notes: json.result.notes,
          // toRead: {
          //   isUrgent: json.result.toRead.isUrgent,
          //   isImportant: json.result.toRead.isImportant
          // }
        }
        setResult({
          isLoading: false,
          bookmark: newBookmark
        });
      })
      .catch((error) => {
        setResult({isLoading: false, bookmark: result.bookmark});
        console.error(error);
      });
    });
  }, []);

  if (result.isLoading) {
    return (
      <section className="section">
        <div className="container">
          <h3 className="subtitle is-3">Loading...</h3>
        </div>
      </section>
    );
  } else if (Object.keys(result.bookmark).length === 0){
    return (
      <section className="section">
        <div className="container">
          <h3 className="subtitle is-3">Bookmark not found</h3>
        </div>
      </section>
    );
  } else {
    return (
      <Show bookmark={result.bookmark} />
    );
  }

}

export default App;
