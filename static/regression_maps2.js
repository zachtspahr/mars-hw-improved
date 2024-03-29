//var query_url = "https://raw.githubusercontent.com/zachtspahr/zachtspahr.github.io/master/2020_congressional_data.json"
//var query_url = "http://127.0.0.1:5000/map_model_geojson"

var query_url =  "https://zach-spahr-politics.herokuapp.com/map_model_geojson"
var api_key = "pk.eyJ1IjoiZGFydGFuaW9uIiwiYSI6ImNqbThjbHFqczNrcjkzcG10cHpoaWF4aWUifQ.GwBz1hO0sY2QE8bXq9pSRg";

var mapboxAccessToken = api_key;
var map = L.map('map').setView([37.8, -96], 4);


L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + mapboxAccessToken, {
    id: 'mapbox/light-v9',
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
}).addTo(map);
//https://api.mapbox.com/styles/v1/mapbox/outdoors-v11.html?title=true&access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4M29iazA2Z2gycXA4N2pmbDZmangifQ.-g_vE53SD2WrJ6tFX7QHmA#2/20/0
var info; 
var legend;



d3.selectAll("#categories").on("change", menu);
function menu() { var selectedCategory = d3.select("#categories option:checked");
var category = selectedCategory.property("value");
console.log(info);
console.log(category);
$(".leaflet-interactive").remove();


if (category == "Biden") {
    winner = "Biden_Expected_Vote";
    winner_actual = "Biden_Actual_Vote";
    president = "Biden";
    elect_type = "Vote Share";
    new_category = 2020;
    

  } else if (category == "Trump"){
    winner = "Trump_Actual_Vote";
    winner_actual = "Trump_Expected_Vote";
    president = "Trump";
    elect_type = "Vote Share"
    new_category = 2020;

}
else if  (category == "Biden_Margin"){
    winner = "Predicted_Biden_Margin";
    winner_actual = "Actual_Biden_Margin";
    president = "Biden";
    elect_type = "Margin";
    new_category = 2020;

  }
  else  {
    console.log("No category selected")
  }



 d3.json(query_url, function(data) {
    house_data = data
    console.log(house_data);
    L.geoJson(house_data).addTo(map);
     
      
      //if (legend instanceof L.Control) { map.removeControl(legend); }
      //if (info instanceof L.Control) { map.removeControl(info); }
      d3.select(".info").remove()

    var info = L.control()


    info.onAdd = function (map) {
        
        this._div = L.DomUtil.create('div', 'info');
        this.update();
        return this._div;
        };

    info.update = function (props) {
    this._div.innerHTML = '<h4> Election Results by House District</h4>' +  (props ?
        '<b>' + props.district + "<br>" + `</b> Predicted ${new_category} ${president} ${elect_type}:<br />` + parseFloat(props[`${winner}`]).toFixed(2) + '%</b> <br />' + `</b>Actual ${new_category} ${president} ${elect_type}:<br />` + parseFloat(props[`${winner_actual}`]).toFixed(2) + '%</b> <br />' 

        : 'Hover over a congressional district');
        };
        
    function getColor(d) {
        return d > 10 ? '#0000ff' :
                d > 5  ? '#3233c4' :
                d > 2.5  ? '#3300cc' :
                d > 0  ? '#4d00b2' :
                d > -2.5  ? '#bf0040' :
                d > -5  ? '#e6001a' :
                d < -10   ? '#ff0000' :
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
        fillColor: getColor(feature.properties[`${winner_actual}`]-feature.properties[`${winner}`])
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
        
        geojson = L.geoJson(house_data, {
            style: style,
            onEachFeature: onEachFeature
        }).addTo(map);
        
        map.attributionControl.addAttribution('Population data &copy; <a href="http://census.gov/">US Census Bureau</a>');
        
        //if (legend != undefined) {
        //map.removeLayer(legend)};
        //map.removeLayer(legend)};
        d3.select(".legend").remove()
        
        var legend = L.control({position: 'bottomright'});
        
        legend.onAdd = function (map) {
           
        
            var div = L.DomUtil.create('div', 'info legend'),
                grades = [-10, -5, -2.5, .001.toFixed(0), 2.5, 5, 10],
                labels = [],
                from, to;
        
            for (var i = 0; i < grades.length; i++) {
                from = grades[i];
                to = grades[i + 1];
        
                labels.push(
                    '<i style="background:' + getColor(from + 1) + '"></i> ' +
                    from + (to ? ' &ndash; ' + to : ' + '));
            }
        
            div.innerHTML = `<h4> ${new_category} ${president} ${elect_type}<br> Performance  Relative to Expectations </h4>` + labels.join('<br>');
            return div;
        
        }
        //if (legend instanceof L.Control) { map.removeControl(legend); }
        //if (info instanceof L.Control) { map.removeControl(info); }
        legend.addTo(map);
        info.addTo(map);
        //if (legend instanceof L.Control) { map.removeControl(legend); }
        //if (info instanceof L.Control) { map.removeControl(info); }
        //if (geojson instanceof L.Control) { map.removeControl(info); }
        
        
    
    
    
    
    });

    
    
}
