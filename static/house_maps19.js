var query_url = "https://raw.githubusercontent.com/zachtspahr/zachtspahr.github.io/master/2020_congressional_data.json"

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


if (category == 2018) {
    winner = "midterm_dem_vote";
    president = "Democratic Party";
    loser = "midterm_gop_vote";
    runner_up = "Republican Party";
    year = "midterm_margin";
    new_category = 2018;
    query_url = "https://raw.githubusercontent.com/zachtspahr/zachtspahr.github.io/master/2018_districts_data.json"
} else if (category == 2020) {
    winner = "2020_dem_pct";
    president = "Democratic Party"
    loser = "2020_gop_pct";
    runner_up = "Republican Party"
    year = "2020_dem_margin";
    new_category = 2020;
    query_url="https://raw.githubusercontent.com/zachtspahr/zachtspahr.github.io/master/2020_congressional_data.json"
  } else {
    winner = "2016_gop_house_pct";
    president = "Republican Party"
    loser = "2016_dem_house_pct";
    runner_up = "Democratic Party"
    year = "2016_dem_house_margin"
    new_category = 2016
    query_url= "https://raw.githubusercontent.com/zachtspahr/zachtspahr.github.io/master/2016_districts_data.json";
    //removeFeature(L.geoJson(),id);
    //map.clearLayers();
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
        '<b>' + props.district + "<br>" + `</b> ${category} ${president} Vote Share:<br />` + parseFloat(props[`${winner}`]).toFixed(2) + '%</b> <br />' + `</b> ${category} ${runner_up}  Vote Share:<br />` + parseFloat(props[`${loser}`]).toFixed(2) + '%</b> <br />'
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
        fillColor: getColor(feature.properties[`${year}`])
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
        //if (geojson instanceof L.Control) { map.removeControl(info); }
        
        
    
    
    
    
    });

    
    
}
