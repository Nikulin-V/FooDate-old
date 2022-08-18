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

function fullScreen() {
    let element = document.getElementsByTagName('body')[0];
    if (element.requestFullscreen) {
        element.requestFullscreen();
    } else if (element.webkitrequestFullscreen) {
        element.webkitRequestFullscreen();
    } else if (element.mozRequestFullscreen) {
        element.mozRequestFullScreen();
    }
}

function fullScreenCancel() {
    if (document.exitFullscreen) {
        document.exitFullscreen();
    } else if (document.webkitExitFullscreen ) {
        document.webkitExitFullscreen();
    } else if (document.mozExitFullscreen) {
        document.mozExitFullScreen();
    }
}

function fullscreenToggle() {
    let fullscreenBtn = $('.fullscreen-btn');
    if (document.fullscreenElement === null) {
        fullScreen();
        fullscreenBtn.attr('src', '/static/images/icons/fullscreen_close.png')
    } else {
        fullScreenCancel();
        fullscreenBtn.attr('src', '/static/images/icons/fullscreen_open.png')
    }
}