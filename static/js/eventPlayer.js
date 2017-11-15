(function setupSessionStorage() {
    sessionStorage.removeItem('sessionId');
    sessionStorage.setItem('event_id', webcastId);
    sessionStorage.setItem('platform', navigator.platform);
    sessionStorage.setItem('device', navigator.userAgent);
    playerInstance.on('pause', function () {
        sessionStorage.setItem('attedance', playerInstance.getPosition())
    });

    $.ajax({

    })
})();

