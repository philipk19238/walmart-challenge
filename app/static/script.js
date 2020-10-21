function create_error(text){
    let error = `<div class="alert alert-danger alert-dismissible fade show" role="alert" style="text-align: center;">
    <strong>${text}</strong>
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>
    </div>`
    return error; 
}

function post(url, data) {
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (this.readyState == XMLHttpRequest.DONE && this.status === 200) {
            let response = xhr.responseText;
            var endpoint = JSON.parse(response)["redirect"];
            window.location.replace(window.origin + endpoint);
        } else {
            let response = xhr.responseText;
            var message = JSON.parse(response)["error"]
            let error = create_error(message);
            document.getElementById("error").innerHTML = error; 
        }
    }
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    console.log(data);
    xhr.send(JSON.stringify(data));
}

function redirect(url){
    const origin = window.origin; 
    window.location.replace(origin + url)
}

function logout(){
    const URL = window.origin + '/logout';
    post(URL, {"data":"data"});
}

function parse_time(time_string){
    let date = time_string.split('T')[0].split('-');
    let [year, month, day] = date;
    return `${month}-${day}-${year}`;
}