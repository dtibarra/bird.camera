window.flipBird = function() {
    document.getElementById("birbLogo").classList.add("animate-flip-horizontal");
}
window.flipBirdMobile = function() {
    document.getElementById("birbLogoMobile").classList.add("animate-flip-horizontal");
}

function getCurrentWeather() {
    fetch('https://bird.camera/current_weather.json')
    .then(response => response.json())
    .then(data => {
        let temperature = data.temperature
        let relativeHumidity = data.relativeHumidity
        let heatIndex = data.heatIndex
        let windSpeed = data.windSpeed
        let windDirection = data.windDirection
        document.getElementById("temperature").textContent = temperature + '°F'
        document.getElementById("relativeHumidity").textContent = relativeHumidity + '%'
        document.getElementById("windSpeed").textContent = windSpeed + ' MPH'
        if (windDirection === null) {
            document.getElementById("windDirection").textContent = ""
        } else {
            document.getElementById("windDirection").textContent = windDirection
        }
        if (heatIndex === null) {
            document.getElementById("heatIndex").textContent = ''
        } else {
            document.getElementById("heatIndex").textContent = '(Feels like '+ heatIndex + '°F)'
        }

        // Polling interval: 5 minutes (adjust this to the desired polling interval)
        setTimeout(getCurrentWeather, 5 * 60 * 1000);
    })
    .catch(err => {
        console.error('Error fetching weather data:', err);
        // Retry interval: 1 minute (adjust this to the desired retry interval)
        setTimeout(getCurrentWeather, 1 * 60 * 1000);
    });
}
if (document.getElementById("temperature")){
    getCurrentWeather();
}
var video = document.getElementById('video');
if (video) {
    var videoSrc = 'https://bird.camera/stream/index.m3u8';
    if (Hls.isSupported()) {
        var hls = new Hls();
        hls.loadSource(videoSrc);
        hls.attachMedia(video);
        video.play();
    }
    // HLS.js is not supported on platforms that do not have Media Source
    // Extensions (MSE) enabled.
    //
    // When the browser has built-in HLS support (check using `canPlayType`),
    // we can provide an HLS manifest (i.e. .m3u8 URL) directly to the video
    // element through the `src` property. This is using the built-in support
    // of the plain video element, without using HLS.js.
    //
    // Note: it would be more normal to wait on the 'canplay' event below however
    // on Safari (where you are most likely to find built-in HLS support) the
    // video.src URL must be on the user-driven white-list before a 'canplay'
    // event will be emitted; the last video event that can be reliably
    // listened-for when the URL is not on the white-list is 'loadedmetadata'.
    else if (video.canPlayType('application/vnd.apple.mpegurl')) {
        video.src = videoSrc;
    }
}

/*if ("serviceWorker" in navigator) {
    // register service worker
    navigator.serviceWorker.register("service-worker.js");
}
self.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        window.location.reload();
    }
});*/
