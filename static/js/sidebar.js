$(document).ready(function() {
    var sb = document.getElementById("sidebar");
    if(sb.childNodes.length <= 2) {
        sb.parentNode.removeChild(sb);
    }
});
