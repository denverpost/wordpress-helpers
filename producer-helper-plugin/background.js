/**
 * Returns a handler which will open a new window when activated.
 */
function getClickHandler(destination){
return function(info, tab){
    source_url = tab.url
    if(source_url == info.srcUrl)
    {
        path_array = source_url.split('/');
        source_url = path_array[0] + "//" + path_array[2];
    }
    chrome.storage.sync.get({ domain: '' },
        function(items) {
            chrome.windows.create({
                "url": items.domain + "/tools/p?url=" + escape(info.srcUrl) + "&source_url=" + escape(source_url) + "&title=" + escape(tab['title']) + "&destination=" + escape(destination),
                'type': 'popup'
            });
    });

  };
};
/**
 * Create a context menu which will only show up for URLs and images.
 */
chrome.contextMenus.create({
  "title" : "Save this URL",
  "type" : "normal",
  "onclick" : getClickHandler("text")
});
chrome.contextMenus.create({
  "title" : "Save this Image",
  "type" : "normal",
  "contexts" : ["image"],
  "onclick" : getClickHandler("picture")
});
