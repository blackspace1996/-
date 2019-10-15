function sendID(id) {
    document.getElementById('user_id').value = id
}

function sendPwd() {
    var csrftoken = getCookie('csrftoken');
    var request = new XMLHttpRequest();
    var url_root = document.getElementById("url_resetPwd").value;
    request.onreadystatechange = function () {
        if (request.readyState === 4) {
            if (request.status === 200) {
                var url = JSON.parse(request.response).url;
                window.alert("更改成功");
                window.location.href = url;
            }
        }
    };
    request.open('post', url_root);
    form = new FormData();
    form.append('user_id', document.getElementById('user_id').value);
    form.append('newPwd', document.getElementById('newPwd').value);
    form.append('csrfmiddlewaretoken', csrftoken);
    request.send(form);

}
