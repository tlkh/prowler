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

sshDisplay = document.getElementById("ssh-count");
vncDisplay = document.getElementById("vnc-count");
telnetDisplay = document.getElementById("telnet-count");
othersDisplay = document.getElementById("others-count");
deviceTable = document.getElementById("device-table");

document.addEventListener('DOMContentLoaded', function () {
    Promise.all([getFirebaseData("/172/22/")]).then(function (results) {
        data = results[0];
        console.log(data);
        subnet = [];
        Object.keys(data).forEach(function (key, index) {
            i = index;
            Object.keys(data[i]).forEach(function (key, index) {
                j = key;
                subnet.push(data[i][j]);
            });
        });
        ssh_count = 0;
        telnet_count = 0;
        vnc_count = 0;
        others = 0;
        Object.keys(subnet).forEach(function (key, index) {
            var row = deviceTable.insertRow(1);
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);
            var cell5 = row.insertCell(4);
            cell1.innerHTML = subnet[key].hostname;
            cell2.innerHTML = subnet[key].status;
            try {
                protocols = subnet[index].services;
                cell3.innerHTML = protocols;
                Object.keys(protocols).forEach(function (key, index) {
                    console.log(protocols[index]);
                    if (protocols[index] == "22/ssh") {
                        ssh_count = ssh_count + 1;
                    } else if (protocols[index] == "80/http" || protocols[index] == "8080/http" || protocols[index] == "8081/http" || protocols[index] == "443/http") {
                        telnet_count = telnet_count + 1;
                    } else if (protocols[index] == "5900/vnc") {
                        vnc_count = vnc_count + 1;
                    } else {
                        others = others + 1
                    }
                });

            } catch (err) {
                cell3.innerHTML = "No open ports";
            }
        });
        renderText(sshDisplay, ssh_count);
        renderText(vncDisplay, vnc_count);
        renderText(telnetDisplay, telnet_count);
        renderText(othersDisplay, others);
    });
});
