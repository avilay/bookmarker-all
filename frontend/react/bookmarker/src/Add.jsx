// @flow

import React from "react";
import type { Node } from "react";
import { useState } from "react";
import { useHistory } from "react-router-dom";

type Bookmark = {
  id: number,
  title: string,
  url: string,
  notes: string,
};

type Props = {
  addBookmark(Bookmark): void
}

function Add(props: Props): Node {
  const [title, setTitle] = useState("");
  const [url, setUrl] = useState("");
  const [notes, setNotes] = useState("");
  let history = useHistory();

  function addClick(e) {
    e.preventDefault();
    props.addBookmark({
      id: 0,
      title: title,
      url: url,
      notes: notes
    });
    history.replace({pathname: "/"});
  }

  function cancelClick(e) {
    e.preventDefault();
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
                <button className="button is-info" onClick={addClick}>Add</button>
                <button className="button" onClick={cancelClick}>Cancel</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );

  // return (
  //   <div className="container" style={{paddingTop: "1%"}}>
  //     <h3>Add Bookmark</h3>

  //     <form>
  //       <label>Title</label>
  //       <input
  //         className="u-full-width"
  //         type="text"
  //         value={title}
  //         onChange={(e) => setTitle(e.target.value)}
  //       />

  //       <label>Url</label>
  //       <input
  //         className="u-full-width"
  //         type="text"
  //         value={url}
  //         onChange={(e) => setUrl(e.target.value)}
  //       />

  //       <label>Notes</label>
  //       <textarea
  //         className="u-full-width"
  //         style={{height: "150px"}}
  //         value={notes}
  //         onChange={(e) => setNotes(e.target.value)}
  //       />

  //       <div className="row">
  //         <div style={{display: "inline", paddingRight: "10px"}}>
  //           <input
  //             className="button-primary"
  //             type="submit"
  //             value="Add"
  //             style={{display: "inline"}}
  //             onClick={addClick}
  //           />
  //         </div>
  //         <div style={{display: "inline", paddingRight: "10px"}}>
  //           <input
  //             className="button"
  //             type="submit"
  //             value="Cancel"
  //             style={{display: "inline"}}
  //             onClick={cancelClick}
  //           />
  //         </div>
  //       </div>
  //     </form>
  //   </div>
  // );
}

export { Add };