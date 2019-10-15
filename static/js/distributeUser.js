function validate() {

    var pwd = document.getElementById("pwd").value;
    var pwd_repeat = document.getElementById("pwd_repeat").value;

    if (pwd == pwd_repeat) {

        document.getElementById("pwd_tip").innerHTML = "<span class=\"glyphicon glyphicon-ok\" aria-hidden=\"true\"></span>";
        document.getElementById("pwd_tip").style.color = "green";

        document.getElementById("register").disabled = false;

    }

    else {

        document.getElementById("pwd_tip").innerHTML = "<span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span>";
        document.getElementById("pwd_tip").style.color = "#CF0070";

        document.getElementById("register").disabled = true;

    }
}

var option_operator = document.getElementById("Operator_company");
var option_sysOperator = document.getElementById("sysOperator_company");
var select_identityClass = document.getElementById("identityClass");
var identity = document.getElementById("identity");
var Operator_company = document.getElementById("company_belong");
var sysOperator_company = document.getElementById("company_bottom");
var company =document.getElementById("company");
if (identity.value == "Operator"){
    select_identityClass.onclick = function () {
       if (select_identityClass.value == 3){
           option_sysOperator.style.display = 'none';
           option_operator.style.display = 'block';
       }
       else{
           option_sysOperator.style.display = 'block';
           option_operator.style.display = 'none';
       }
    };

    Operator_company.onchange = function () {
        company.value = Operator_company.value;
    };

    sysOperator_company.onchange = function () {
        company.value = sysOperator_company.value;
    };}
