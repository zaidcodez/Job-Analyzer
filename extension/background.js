chrome.runtime.onInstalled.addListener(() => {
    console.log("PakTech Job Copilot Extension Installed");
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "ping") {
        sendResponse({ status: "alive" });
    }
});