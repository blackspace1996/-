function validate() {

    var pwd = document.getElementById("newPwd").value;
    var pwd_repeat = document.getElementById("newPwd_repeat").value;

    if (pwd == pwd_repeat) {

        document.getElementById("pwd_tip").innerHTML = "<span class=\"glyphicon glyphicon-ok\" aria-hidden=\"true\"></span>";
        document.getElementById("pwd_tip").style.color = "green";

        document.getElementById("update").disabled = false;

    }

    else {

        document.getElementById("pwd_tip").innerHTML = "<span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span>";
        document.getElementById("pwd_tip").style.color = "#CF0070";

        document.getElementById("update").disabled = true;

    }
}

