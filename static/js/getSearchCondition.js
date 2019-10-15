function searchSubmit(){
   var searchCondition = document.getElementById("search");
   var url = '?search=' + searchCondition.value;
   window.location.href = url;
}