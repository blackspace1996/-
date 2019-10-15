function getCurrentCompany(){
   var query = document.getElementById("company_query");
   var url = '?company_current=' + query.value;
   window.location.href = url;
}