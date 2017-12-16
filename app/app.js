// Initialize Firebase
var config = {
    apiKey: "AIzaSyCOhJuPsdThHoPghb3LxwVJv9WJVyRIYms",
    authDomain: "clusterscanner.firebaseapp.com",
    databaseURL: "https://clusterscanner.firebaseio.com",
    projectId: "clusterscanner",
    storageBucket: "clusterscanner.appspot.com",
    messagingSenderId: "169655797012"
};
firebase.initializeApp(config);

email = "fake@fake.com";
password = "totallyLegit";

firebase.auth().signInWithEmailAndPassword(email, password).catch(function (error) {
    var errorCode = error.code;
    var errorMessage = error.message;
});

// Get a reference to the database service
var database = firebase.database();
console.log("Connection to Firebase established.");

var firebaseData = {};

function getFirebaseData(endpoint) {
    return firebase.database().ref(endpoint).once("value", function (snapshot) {
        return snapshot.val();
    });
}

function renderText(element, statusText) {
    element.textContent = statusText;
}

function getFirebaseData(url) {
    return firebase.database().ref(url).once('value').then(function (snapshot) {
        var data = (snapshot.val());
        return data;
    });
}

domainDisplay = document.getElementById("domain");


document.addEventListener('DOMContentLoaded', function () {
    Promise.all([getFirebaseData("/172/22/")]).then(function (results) {
        data = results[0];
        subnet = [];
        Object.keys(data).forEach(function (key, index) {
            i = index;
            Object.keys(data[i]).forEach(function (key, index) {
                j = index;
                subnet.push(data[i][j]);
            });
        });
        console.log(subnet);
    });
});
