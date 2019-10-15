function task(){
   var taskType = document.getElementById("taskType");
   var getTaskURL = '?taskType=' + taskType.value;
   window.location.href = getTaskURL;
}

function getReceivingTask(){
   var filter = document.getElementById("filter-receiving");
   var order = document.getElementById("orderStore").value;
   var taskType = document.getElementById("taskTypeStore").value;
   if (filter.checked == true){
      var getReceivingTaskURL = '?receiving=true&order=' + order + '&taskType=' + taskType;
      window.location.href = getReceivingTaskURL;
   }
   else{
      var getTaskURL = '?receiving=false&order=' + order + '&taskType=' + taskType;
      window.location.href = getTaskURL;
   }


}

function receiveCompanyTaskID(id) {
    var id_input = document.getElementById("task_id");
    id_input.value = id;
}

function urlSubmit(){
   var id_input = document.getElementById("task_id");
   var url_root = document.getElementById("url_root");
   var url = url_root.value + '?id=' + id_input.value;
   console.log(url);
   window.location.href = url;
}