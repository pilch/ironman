mapboxgl.accessToken = 'pk.eyJ1IjoiZHJlaWRwaWxjaCIsImEiOiJjaXJqZ2MzcWUwMDFjZmZtNndid2MyZ2Y2In0.v4zf2aCdnopAFaqXJ97SzA';

var startCoords = [-73.983,44.285];
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v10',
    center: startCoords,
    zoom: 8
});

// Create a GeoJSON source with an empty lineString.
var geojson = {
    "type": "FeatureCollection",
    "features": [{
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                startCoords
            ]
        }
    }]
};

var speedFactor = 300; // number of frames per longitude degree
var animation; // to store and cancel the animation
var startTime = 0;
var progress = 0; // progress = timestamp - startTime
var resetTime = false; // indicator of whether time reset is needed for the animation
var pauseButton = document.getElementById('pause');

map.on('load', function() {

    // add the line which will be modified in the animation
    map.addLayer({
        'id': 'line-animation',
        'type': 'line',
        'source': {
            'type': 'geojson',
            'data': geojson
        },
        'layout': {
            'line-cap': 'round',
            'line-join': 'round'
        },
        'paint': {
            'line-color': '#ed6498',
            'line-width': 5,
            'line-opacity': .8
        }
    });

    startTime = performance.now();

    animateLine();

    // click the button to pause or play
    pauseButton.addEventListener('click', function() {
        pauseButton.classList.toggle('pause');
        if (pauseButton.classList.contains('pause')) {
            cancelAnimationFrame(animation);
        } else {
            resetTime = true;
            animateLine();
        }
    });

    // reset startTime and progress once the tab loses or gains focus
    // requestAnimationFrame also pauses on hidden tabs by default
    document.addEventListener('visibilitychange', function() {
        resetTime = true;
    });

    // animated in a circle as a sine wave along the map.
    function animateLine(timestamp) {
        if (resetTime) {
            // resume previous progress
            startTime = performance.now() - progress;
            resetTime = false;
        } else {
            progress = timestamp - startTime;
        }

        // restart if it finishes a loop
        if (progress > speedFactor * 30) {
            startTime = timestamp;
            geojson.features[0].geometry.coordinates = [];
            geojson.features[0].geometry.coordinates.push(startCoords);
            console.log(geojson.features[0].geometry.coordinates);
        } else {
            var x = progress / speedFactor + startCoords[0];
            // draw a sine wave with some math.
            var y = startCoords[1] + Math.sin(x*Math.PI/90);
            // append new coordinates to the lineString
            geojson.features[0].geometry.coordinates.push([x, y]);
            // then update the map
            map.getSource('line-animation').setData(geojson);
        }
        // Request the next frame of the animation.
        animation = requestAnimationFrame(animateLine);
    }
});