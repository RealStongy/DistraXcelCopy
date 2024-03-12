chrome.runtime.onMessage.addListener(function(message, send, sendResponse) {
    // chrome.tabs.sendMessage()
});

// banned urls
const bannedUrls = [
    "*://*.facebook.com/*",
    "https://www.instagram.com/",
    "https://www.twitter.com/",
    "https://www.reddit.com/",
]

function urlMatches(url, pattern) {
    const patternParts = pattern.split('*');
    return patternParts.every((part) => url.includes(part));
}

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    console.log("TAB UPDATED");
    if (changeInfo.url) {
        console.log("URL CHANGED: " + changeInfo.url);
        for (const target of bannedUrls) {
            console.log(target);
            if (urlMatches(changeInfo.url, target)) {
                chrome.tabs.remove(tabId);
                break;
            }
        }
    }
});

try {
    self.importScripts("firebase/firebase-app.js", "firebase/firebase-auth.js");

    const firebaseConfig = {
        apiKey: "AIzaSyC66jG3fuMmq7prgdGvKYI7UbvxcAD2y-Q",
        authDomain: "distraxcel.firebaseapp.com",
        databaseURL: "https://distraxcel-default-rtdb.firebaseio.com",
        projectId: "distraxcel",
        storageBucket: "distraxcel.appspot.com",
        messagingSenderId: "233080846634",
        appId: "1:233080846634:web:bf3688519b3062a7338653",
        measurementId: "G-CQ8QTLGJXH"
    };

    firebase.initializeApp(firebaseConfig);
    console.log("Firebase is initialized");

    chrome.runtime.onMessage.addListener((msg, sender, resp) => {
        if (msg.command == "login") {
            console.log("Attempting to login user " + msg.email + " with password: " + msg.password);
            firebase.auth().signInWithEmailAndPassword(msg.email, msg.password).then(function() {
                console.log("Firebase login success!");
                resp({result: "success"});
            }).catch(function(error) {
                console.log("Something went wrong");
                resp({result: "failure"});
            });
            return true;
        }
    });

} catch (e) {
    console.error(e);
}