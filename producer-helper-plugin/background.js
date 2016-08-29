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

function insertSidebar(sidebar) {
    return function(info, tab) {
        console.log(info)
        console.log(tab)
    };
};
/**
 * Create a context menu for all that we desire
 */
chrome.contextMenus.create({
  "title" : "Insert weather sidebar",
  "type" : "normal",
  "onclick" : insertSidebar("weather")
});
