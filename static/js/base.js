window.onload=function () {
    var lis = document.getElementsByTagName("li");
    var subaside = document.getElementsByClassName("subAside");

    for (var i = 0; i < 12; i++) {
        lis[i+5].setAttribute("Number", i);
        lis[i+5].onmousemove = function () {
            subaside[this.getAttribute("Number")].style.display = 'block';
        };
        lis[i+5].onmouseleave = function () {
            subaside[this.getAttribute("Number")].style.display = 'none';
        };
    }
}