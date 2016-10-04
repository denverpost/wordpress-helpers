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
    console.log('hi');
    console.log(sidebar);
    if ( document.getElementById('content') )
    {
        // We have a textarea, lets put something into it.
        console.log(document.getElementById('content'))
    }
    return function(info, tab) {
        console.log(info)
        console.log(tab)
    };
};
/**
 * Create a context menu for all that we desire
 */
chrome.contextMenus.create({
  "title" : "Insert sidebar",
  "type" : "normal",
  "onclick" : insertSidebar("weather")
});
