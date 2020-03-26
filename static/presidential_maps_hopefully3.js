var api_key = "pk.eyJ1IjoiZGFydGFuaW9uIiwiYSI6ImNqbThjbHFqczNrcjkzcG10cHpoaWF4aWUifQ.GwBz1hO0sY2QE8bXq9pSRg";

var mapboxAccessToken = api_key;
var map = L.map('map').setView([37.8, -96], 4);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + mapboxAccessToken, {
    id: 'mapbox/light-v9',
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
}).addTo(map);

var info; 
var legend;



d3.selectAll("#categories").on("change", menu);
function menu() { var selectedCategory = d3.select("#categories option:checked");
var category = selectedCategory.property("value");
console.log(category);


if (category == 2000) {
    winner = "Bush_Pct_00";
    president = "Bush"
    loser = "Gore_Pct_00";
    runner_up = "Gore"
    year = "Dem_Margin_00";
    new_category = 2000
  } else if (category == 2004) {
    winner = "Bush_Pct_04";
    president = "Bush"
    loser = "Kerry_Pct_04";
    runner_up = "Kerry"
    year = "Dem_Margin_04";
    new_category = 2004
  } else if (category == 2008) {
    winner = "Obama_Pct_08";
    president = "Obama"
    loser = "McCain_Pct_08";
    runner_up ="McCain"
    year = "Dem_Margin_08";
    new_category = 2008
  
  }else if (category == 2012) {
    winner = "Obama_Pct_12";
    president = "Obama"
    loser = "Romney_Pct_12";
    runner_up = "Romney"
    year = "Dem_Margin_12";
    new_category = 2012
  
  } else {
    winner = "Trump_Pct_16";
    president = "Trump"
    loser = "Clinton_Pct_16";
    runner_up = "Clinton"
    year = "Dem_Margin_16";
    new_category = 2016
  }



var query_url = "http://127.0.0.1:5000/senate_api"

  d3.json(query_url, function(data) {
      senate_data = data
      console.log(senate_data);
      L.geoJson(senate_data).addTo(map);
     
      
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
    this._div.innerHTML = '<h4>State Election Results</h4>' +  (props ?
        '<b>' + props.name + "<br>" + `</b> ${category} ${president} Vote Share:<br />` + parseFloat(props["Past_Election_Results"][`${winner}`]).toFixed(2) + '%</b> <br />' + `</b> ${category} ${runner_up}  Vote Share:<br />` + parseFloat(props["Past_Election_Results"][`${loser}`]).toFixed(2) + '%</b> <br />'
        : 'Hover over a state');
        };
        
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
        fillColor: getColor(feature.properties.Past_Election_Results[`${year}`])
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
        
        geojson = L.geoJson(senate_data, {
            style: style,
            onEachFeature: onEachFeature
        }).addTo(map);
        
        map.attributionControl.addAttribution('Population data &copy; <a href="http://census.gov/">US Census Bureau</a>');
        
        //if (legend != undefined) {
        //map.removeLayer(legend)};
        d3.select(".legend").remove()
        
        var legend = L.control({position: 'bottomright'});
        
        legend.onAdd = function (map) {
           
        
            var div = L.DomUtil.create('div', 'info legend'),
                grades = [-100, -20, -10, .001.toFixed(0), 10, 20, 30],
                labels = [],
                from, to;
        
            for (var i = 0; i < grades.length; i++) {
                from = grades[i];
                to = grades[i + 1];
        
                labels.push(
                    '<i style="background:' + getColor(from + 1) + '"></i> ' +
                    from + (to ? ' &ndash; ' + to : ' + '));
            }
        
            div.innerHTML = `<h4> ${new_category} Dem Margin</h4>` + labels.join('<br>');
            return div;
        
        }
        //if (legend instanceof L.Control) { map.removeControl(legend); }
        //if (info instanceof L.Control) { map.removeControl(info); }
        legend.addTo(map);
        info.addTo(map);
        //if (legend instanceof L.Control) { map.removeControl(legend); }
        //if (info instanceof L.Control) { map.removeControl(info); }
        
        
    
    
    
    
    });

    
    
}
