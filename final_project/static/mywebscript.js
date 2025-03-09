let RunSentimentAnalysis = () => {
    let textToAnalyze = document.getElementById("textToAnalyze").value;

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && (this.status == 200 || this.status == 400)) {
            document.getElementById("system_response").innerHTML = xhttp.responseText;
        }
    };
    // Use POST instead of GET.
    xhttp.open("POST", "emotionDetector", true);
    // Set header to send form data.
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    // Use the parameter name expected by the server ('statement').
    xhttp.send("statement=" + encodeURIComponent(textToAnalyze));
}
