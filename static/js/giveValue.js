function giveValue(){
    var sort_form = document.getElementById("sort_form");
    var sort_list = document.getElementsByClassName("list-group-item");
    var sort_input = document.getElementsByClassName("sort_input");
    var measureAmount = parseInt(document.getElementById("measureAmount").value);
    var i;
    for(i=0;i<measureAmount;i++){
        sort_input[i].setAttribute("temp",sort_list[i].id);
    }
    for(i=0;i<measureAmount;i++){
        sort_input[i].value = sort_input[i].getAttribute("temp");
    }
    sort_form.submit()
    // sort_input[0].value = sort_list[0].id;
    // console.log(sort_input[0].value);

}
