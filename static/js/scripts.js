function getUrlParameter(sParam) {
    let sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;
    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
    return false;
}

function setRedirectTimer(elementId, link, seconds) {
    $(document).ready(
        function () {
            element = $('#' + elementId);
            element.html(seconds);
            setInterval(function () {
                element.html(--seconds);
            }, 1000);
            setTimeout(function () {
                document.location.href = link
            }, seconds * 1000)
        }
    )
}
