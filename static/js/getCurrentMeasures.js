function getCurrentCompany(){
   var query = document.getElementById("company_query");
   var jumpURL = '?company_current=' + query.value;
   window.location.href = jumpURL;
}

function getCurrentRawProduction(){
   var query = document.getElementById("company_query");
   var production = document.getElementById("rawProduction_current");
   var jumpURL = '?company_current=' + query.value + '&rawProduction_current=' + production.value;
   window.location.href = jumpURL;
}

function getCurrentRawProduction_operator() {
   var production = document.getElementById("rawProduction_current");
   var jumpURL = '?rawProduction_current=' + production.value;
   window.location.href = jumpURL;
}