<script src="https://www.gstatic.com/firebasejs/4.8.0/firebase.js"></script>
<script>
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
</script>

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


function getArticle(data) {
    var a = document.createElement('a');
    a.href = data;
    url = a.href;
    url = url.replace("https://", "");
    url = url.replace("http://", "");
    url = url.replace("/", "");
    url = url.replace(".", "");
    url = url.replace("#", "");
    url = url.replace("?", "");
    console.log(url);
    return url;
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
scoreDisplay = document.getElementById("score");
domainLevel = document.getElementById("domain_level");
articleLevel = document.getElementById("article_level");
display1 = document.getElementById("debug1");


document.addEventListener('DOMContentLoaded', function () {
    getCurrentTabUrl(function (url) {
        var article_url = getURL(url);
        var domain = getDomain(url);
        renderText(domainDisplay, domain);
        console.log(article_url + " - " + domain);
        article_url = article_url.replace(domain, "");
        article_url = article_url.replace("https://", "");
        article_url = article_url.replace("http://", "");
        article_url = article_url.replace(/\//g, "");
        article_url = article_url.replace(".", "");
        article_url = article_url.replace("#", "");
        article_url = article_url.replace("?", "");
        domain = domain.replace(".","")
        domain = domain.replace(".","")
        console.log("final url: " + article_url);
        var url = "/articles/" + domain + "/" + article_url;
        console.log(url);
        Promise.all([getFirebaseData(url)]).then(function (results) {
            data = results[0]
            console.log(data);
            var polarity = data.polarity;
            var subjectivity = data.subjectivity;
            //determine score
            if (domain=="wwwstraitstimescom" || domain=="wwwchannelnewsasiacom") {
                var domain_score = 0.3;
            } else {
                if (domain == "wwwallsingaporestuffcom") {
                var domain_score = 0.1;
            } else {
                var domain_score = 0.15;
            }
            }
            
            var nlp_score = (1 - Math.abs(polarity) / 2 - subjectivity / 2) / 3;
            var vote_score = 0.15;
            var score = domain_score + nlp_score + vote_score;
            mainBox = document.getElementById("box");
            
            if (score > 0.5) {
                renderText(articleLevel, "moderately");
                mainBox.classList.add('alert-success');
                chrome.browserAction.setIcon({path: "../green.png"});
            } else {
                renderText(articleLevel, "not");
                mainBox.classList.add('alert-danger');
                chrome.browserAction.setIcon({path: "../red.png"});
            }
            renderText(scoreDisplay, Math.floor(score * 100));
            if (domain_score > 0.15) {
                renderText(domainLevel, "moderately");
            } else {
                renderText(domainLevel, "not");
            }

        });
    });

});
