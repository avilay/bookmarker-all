chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message === 'get-url') {
    chrome.tabs.query({ active: true, currentWindow: true })
    .then((tabs) => {
      if (tabs === undefined) {
        sendResponse("");
      } else {
        sendResponse(tabs[0].url);
      }
    })
    .catch((error) => {
      console.log("background: Caught error: ", error);
      sendResponse(error);
    });

    return true;
  }
});
