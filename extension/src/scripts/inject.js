export async function getCurrentTab() {
  let queryOptions = { active: true, currentWindow: true };
  let [tab] = await chrome.tabs.query(queryOptions);
  return tab;
}

export async function currTabUrl() {
  return chrome.scripting
    .executeScript({
      target: { tabId: (await getCurrentTab()).id },
      func: () => {
        return document.URL
      },
    })
    .then((injectionResults) => {
      let url = null;
      for (const { result } of injectionResults) {
        url = new URL(result).origin;
      }
      return url;
    });
}
