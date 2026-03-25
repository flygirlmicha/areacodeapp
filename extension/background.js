// Create context menu items when the extension is installed
chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        id: "lookup_areacode",
        title: "Lookup Area Code: \"%s\"",
        contexts: ["selection"],
    });
    chrome.contextMenus.create({
        id: "lookup_domain",
        title: "Lookup Domain WHOIS: \"%s\"",
        contexts: ["selection"],
    });
    chrome.contextMenus.create({
        id: "lookup_ip",
        title: "Lookup IP Geolocation: \"%s\"",
        contexts: ["selection"],
    });
});

// When a context menu item is clicked, store the action and open the popup
chrome.contextMenus.onClicked.addListener((info) => {
    const text = info.selectionText.trim();

    const actionMap = {
        lookup_areacode: { action: "areacode", value: text },
        lookup_domain:   { action: "domain",   value: text },
        lookup_ip:       { action: "ip",        value: text },
    };

    const pending = actionMap[info.menuItemId];
    if (!pending) return;

    // Store the pending lookup so the popup can pick it up when it opens
    chrome.storage.local.set({ pendingLookup: pending }, () => {
        chrome.action.openPopup();
    });
});
