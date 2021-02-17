initialise();

google.maps.event.addDomListener(window, 'load', initialise);
    function initialise() {
        // Basic options for a simple Google Map
        // For more options see: https://developers.google.com/maps/documentation/javascript/reference#MapOptions
             lat = document.getElementById('loc_lat').value;
             long = document.getElementById('loc_long').value;
        
            //var myLatLng = new google.maps.LatLng(12.972744, 80.213812);
           var myLatLng1 = new google.maps.LatLng(lat,long);
            var mapOptions = {
                zoom: 15,
                center: myLatLng1,
                disableDefaultUI: true,
                scrollwheel: false,
                navigationControl: true,
                mapTypeControl: false,
                scaleControl: false,
                draggable: true,
    
            // How you would like to style the map. 
            // This is where you would paste any style found on Snazzy Maps.
            styles: [{
                featureType: 'water',
                stylers: [{
                    color: '#46bcec'
                }, {
                    visibility: 'on'
                }]
            }, {
                featureType: 'landscape',
                stylers: [{
                    color: '#f2f2f2'
                }]
            }, {
                featureType: 'road',
                stylers: [{
                    saturation: -100
                }, {
                    lightness: 45
                }]
            }, {
                featureType: 'road.highway',
                stylers: [{
                    visibility: 'simplified'
                }]
            }, {
                featureType: 'road.arterial',
                elementType: 'labels.icon',
                stylers: [{
                    visibility: 'off'
                }]
            }, {
                featureType: 'administrative',
                elementType: 'labels.text.fill',
                stylers: [{
                    color: '#444444'
                }]
            }, {
                featureType: 'transit',
                stylers: [{
                    visibility: 'off'
                }]
            }, {
                featureType: 'poi',
                stylers: [{
                    visibility: 'off'
                }]
            }]
        };
      
        // Get the HTML DOM element that will contain your map 
        // We are using a div with id="map" seen below in the <body>
        var mapElement = document.getElementById('map-canvass');
        //var mapElement1 = document.getElementById('map-canvas1');
    
        // Create the Google Map using our element and options defined above
        var map = new google.maps.Map(mapElement, mapOptions);
       // var map1 = new google.maps.Map(mapElement1, mapOptions1);
    
        // Let's also add a marker while we're at it
     
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(lat,long),
            map: map,
        });
      
    }

    var wow = new WOW ({
        offset:       75,          // distance to the element when triggering the animation (default is 0)
        mobile:       false,       // trigger animations on mobile devices (default is true)
    });
    wow.initialise();    
    

