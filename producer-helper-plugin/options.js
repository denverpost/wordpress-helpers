// Saves options to chrome.storage
function save_options() {
    var varname = document.getElementById('varname').value;
    chrome.storage.sync.set({
        //varname: varname,
    }, function() {
        // Update status to let user know options were saved.
        var status = document.getElementById('status');
        status.textContent = 'Options saved.';
        setTimeout(function() {
            status.textContent = '';
        }, 750);
    });
}

// Restores select box and checkbox state using the preferences
// stored in chrome.storage.
function restore_options() {
    chrome.storage.sync.get({
        //varname: 'default'
    }, function(items) {
        //document.getElementById('varname').value = items.varname;
    });
}
document.addEventListener('DOMContentLoaded', restore_options);
document.getElementById('save').addEventListener('click', save_options);
