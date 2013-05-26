<?php

print <<<END
<html>
<head>
<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.5/leaflet.css" />
 <!--[if lte IE 8]>
    <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.5/leaflet.ie.css" />
<![endif]-->
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js" ></script>
<script src="http://cdn.leafletjs.com/leaflet-0.5/leaflet.js"></script>
<style type="text/css">
#map { height: 400px; }
</style> 
</head>
<body>

<div id="map"></div>
<div id="msg"></div>

<script type="text/javascript"> 
//define icon for marker
var popsicle = L.icon({
    iconUrl: 'icon.png',
    //shadowUrl: 'leaf-shadow.png',
    iconSize:     [48, 48], // size of the icon
    shadowSize:   [0, 0], // size of the shadow
    iconAnchor:   [24, 48], // point of the icon which will correspond to marker's location
    shadowAnchor: [24, 48],  // the same for the shadow
    popupAnchor:  [0, -48] // point from which the popup should open relative to the iconAnchor
});
//get data from DB
var data = {};

END;
print '$.post("http://playground.sam-d.com/ice/query.php",{"lat":'.$_POST['lat'].',"lon":'.$_POST['lon'].',"dist":'.$_POST['dist'].'}, function(obj)';
print <<<END
     {
        window.data = obj;
     },
 'json').done(function(bla){
    // create map
    var map = L.map('map').setView([data.user.lat, data.user.lon], 13);
    //L .tileLayer('http://a.tile.openstreetmap.org/{z}/{x}/{y}.png'
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
    L.marker([data.user.lat, data.user.lon]).addTo(map)

    if(data.success != true){
        document.getElementById('msg').innerHTML = "No ice cream in a radius of "+data.user.dist+" km around you. Did you check your freezer?";
    }else{
        var table ="<table>";
        table = table+"<thead><tr><th>Name</th><th>Entfernung (km)</th></tr></tbody>"
        for(var i=0; i < data.results.length; i++){
            var obj = data.results[i];
            var mark = L.marker([obj.lat,obj.lon],{icon:popsicle}).addTo(map).bindPopup(obj.name);
            if( i == 0){
                mark.openPopup();
            }
            table = table+"<tr><td>"+obj.name+"</td>"+"<td>"+obj.distance+"</td></tr>";
        }
        table = table+"</tbody></table>"
        document.getElementById('msg').innerHTML = table;
    }
});
</script>

</body>
</html>
END;
?>
