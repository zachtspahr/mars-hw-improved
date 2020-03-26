var api_key = "pk.eyJ1IjoiZGFydGFuaW9uIiwiYSI6ImNqbThjbHFqczNrcjkzcG10cHpoaWF4aWUifQ.GwBz1hO0sY2QE8bXq9pSRg";

var mapboxAccessToken = api_key;
var map = L.map('map').setView([37.8, -96], 4);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + mapboxAccessToken, {
    id: 'mapbox/light-v9',
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
}).addTo(map);

var query_url = "http://127.0.0.1:5000/house_api"

  d3.json(query_url, function(data) {
      cd_data = data
      console.log(cd_data);

      L.geoJson(cd_data).addTo(map);

    var info = L.control()

    info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info');
        this.update();
        return this._div;
        };

    info.update = function (props) {
    this._div.innerHTML = '<h4>Congressional District</h4>' +  (props ?
        '<b>' + props.district + '</b> 2018 Dem Vote Share:<br />' + parseFloat(props.midterm_dem_vote).toFixed(2) + '%</b> <br />' + '</b> 2018 GOP Vote Share:<br />' + parseFloat(props.midterm_gop_vote).toFixed(2) + '%</b> <br />'
        : 'Hover over a district');
        };
        info.addTo(map);
    function getColor(d) {
        return d > 30 ? '#0000ff' :
                d > 20  ? '#3233c4' :
                d > 10  ? '#3300cc' :
                d > 0  ? '#4d00b2' :
                d > -10  ? '#bf0040' :
                d > -20  ? '#e6001a' :
                d < -20   ? '#ff0000' :
                            '#ff0000';
        }
        //750,300,100,50,30
    function style(feature) {
        return {
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7,
        fillColor: getColor(feature.properties.midterm_margin)
            };
        }
        function highlightFeature(e) {
            var layer = e.target;
        
            layer.setStyle({
                weight: 5,
                color: '#666',
                dashArray: '',
                fillOpacity: 0.7
            });
        
            if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
                layer.bringToFront();
            }
        
            info.update(layer.feature.properties);
        }
        
        var geojson;
        
        function resetHighlight(e) {
            geojson.resetStyle(e.target);
            info.update();
        }
        
        function zoomToFeature(e) {
            map.fitBounds(e.target.getBounds());
        }
        
        function onEachFeature(feature, layer) {
            layer.on({
                mouseover: highlightFeature,
                mouseout: resetHighlight,
                click: zoomToFeature
            });
        }
        
        geojson = L.geoJson(cd_data, {
            style: style,
            onEachFeature: onEachFeature
        }).addTo(map);
        
        map.attributionControl.addAttribution('Population data &copy; <a href="http://census.gov/">US Census Bureau</a>');
        
        
        var legend = L.control({position: 'bottomright'});
        
        legend.onAdd = function (map) {
        
            var div = L.DomUtil.create('div', 'info legend'),
                grades = [-100, -20, -10, .001, 10, 20, 30],
                labels = [],
                from, to;
        
            for (var i = 0; i < grades.length; i++) {
                from = grades[i];
                to = grades[i + 1];
        
                labels.push(
                    '<i style="background:' + getColor(from + 1) + '"></i> ' +
                    from + (to ? ' &ndash; ' + to : ' + '));
            }
        
            div.innerHTML = '<h4>Dem Margin</h4>' + labels.join('<br>');
            return div;
        };
        
        legend.addTo(map);
    
    
    
    
    });