function delID(id) {
    var id_input = document.getElementById("delete_id");
    id_input.value = id;
}

function urlSubmit_delete() {
   var id_input = document.getElementById("delete_id");
   var url_root = document.getElementById("url_root");
   var url = url_root.value + '?id=' + id_input.value;
   console.log(url);
   window.location.href = url;
}