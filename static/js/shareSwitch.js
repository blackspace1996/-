var share = document.getElementById("share");
var shareCondition = document.getElementById("conditionContent");

if (share.value == "1"){
    shareCondition.style.display = 'block';}
else{
    shareCondition.style.display = 'None';
}

share.onchange = function () {
    if (share.value == "1"){
        shareCondition.style.display = 'block';}
    else{
        shareCondition.style.display = 'None';
    }
};