
// request.open('GET', 'https://api.fda.gov/drug/event.json?limit=1');
// request.send();

// request.onload = function() {
//     if (request.status === 200) {
//         const data = JSON.parse(request.response);
//         console.log(data);
//     } else {
//         console.log('error');
//     }
// };

function searchMedication(){
    var medName = document.getElementById("medName").value;
    var request = new XMLHttpRequest();
    console.log('HTTP');

    request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText);
            displayResult(data);
        } else {
            console.log('error');
        }
    };

    request.open('GET', 'https://api.fda.gov/drug/label.json?search=openfda.brand_name:' + medName);
    request.send();

    // request.onload = function() {
    //     if (request.status === 200) {
    //         const data = JSON.parse(request.response);
    //         console.log(data);
    //     } else {
    //         console.log('error');
    //     }
    // };

    function displayResult(data) {
        var resultDiv = document.getElementById("result");
        var html = "";
        for (var key in data.results[0]) {
            html += "<p><strong>" + key + ":</strong> " + data.results[0][key] + "</p>";
        }
        resultDiv.innerHTML = html;
    }
}