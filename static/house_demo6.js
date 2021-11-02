var query_url = "https://raw.githubusercontent.com/zachtspahr/zachtspahr.github.io/master/2020_congressional_data.json"

var api_key = "pk.eyJ1IjoiZGFydGFuaW9uIiwiYSI6ImNqbThjbHFqczNrcjkzcG10cHpoaWF4aWUifQ.GwBz1hO0sY2QE8bXq9pSRg";

var mapboxAccessToken = api_key;
var map = L.map('map').setView([37.8, -96], 4);
const rgb = [255, 0, 0];


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

// categories are white_pct, black_pct, native_american_pct, hispanic_pct, asian_pct,
// white_college_pct, white_no_college_pct, cook_pvi, median_income, and pct_BA
if (category == "white_pct") {
    winner = "pct_white";
    race = "white";
    new_category = "white_pct";
    random=""
    verb= "is"
    function getColor(d) {
    rgb[0] = Math.round(d/100 * 255);
    rgb[1] = Math.round(d/100 * 255);
    rgb[2] = Math.round(d/100 * 255);
    return 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')'
                } 
} else if (category == "black_pct") {
    winner = "pct_black";
    race = "black"
    new_category = "black_pct";
    random=""
    verb= "is"
    function getColor(d) {
        rgb[0] = Math.round(255-(d/100 * 255));
        rgb[1] = Math.round(255-(d/100 * 255));
        rgb[2] = Math.round(255-(d/100 * 255));
        return 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')'
                } 
} else if (category == "hispanic_pct") {
    winner = "pct_latino";
    race = "hispanic"
    new_category = "hispanic_pct";
    random=""
    verb= "is"
    function getColor(d) {
        rgb[0] = Math.round(255-(d/100 * 255));
        rgb[1] = Math.round(255-(d/100 * 255));
        rgb[2] = Math.round(255-(d/100 * 255));
        return 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')'
                } 
} else if (category == "asian_pct") {
    winner = "pct_asian";
    race = "asian american"
    new_category = "asian_pct";
    random=""
    verb= "is"
    function getColor(d) {
        rgb[0] = Math.round(255-(d/100 * 255));
        rgb[1] = Math.round(255-(d/100 * 255));
        rgb[2] = Math.round(255-(d/100 * 255));
        return 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')'
                } 
}else if (category == "native_american_pct") {
    winner = "pct_native_american";
    race = "native american"
    new_category = "native_american_pct";
    random=""
    verb= "is"
    function getColor(d) {
        rgb[0] = Math.round(255-(d/100 * 255));
        rgb[1] = Math.round(255-(d/100 * 255));
        rgb[2] = Math.round(255-(d/100 * 255));
        return 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')'
                } 
}else if (category == "other_race_pct") {
    winner = "pct_other_race";
    race = "another race"
    new_category = "other_race_pct";
    random=""
    verb= "is"
    function getColor(d) {
        rgb[0] = Math.round(255-(d/100 * 255));
        rgb[1] = Math.round(255-(d/100 * 255));
        rgb[2] = Math.round(255-(d/100 * 255));
        return 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')'
                } 
}else if (category == "ba_pct") {
    winner = "pct_BA";
    race = "college-educated"
    new_category = "ba_pct";
    random=""
    verb= "has"
    function getColor(d) {
        rgb[0] = Math.round(255-(d/100 * 255));
        rgb[1] = Math.round(255-(d/100 * 255));
        rgb[2] = Math.round(255-(d/100 * 255));
        return 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')'
                } 
}else if (category == "white_college_pct") {
    winner = "pct_white_college";
    race = "a college degree"
    new_category = "white_college_pct";
    random = "white people in"
    verb= "have"
    function getColor(d) {
        rgb[0] = Math.round(255-(d/100 * 255));
        rgb[1] = Math.round(255-(d/100 * 255));
        rgb[2] = Math.round(255-(d/100 * 255));
        return 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')'
                } 
}else //if (category == white_non_college_pct) 
{
    winner = "white_non_college";
    race = "a college degree"
    new_category = "white_non_college_pct";
    random=""
    verb="does not have"
    function getColor(d) {
        rgb[0] = Math.round(d/100 * 255);
        rgb[1] = Math.round(d/100 * 255);
        rgb[2] = Math.round(d/100 * 255);
        return 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')'}
}
  //else {
    //winner = "2016_gop_house_pct";
    //race = "Republican Party"
    //loser = "2016_dem_house_pct";
    //runner_up = "Democratic Party"
    //year = "2016_dem_house_margin"
    //new_category = 2016
    //removeFeature(L.geoJson(),id);
    //map.clearLayers();
  //}



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
            '<b>' + props.district + "<br>" + `</b> Pct of ${random} ${props.district} that ${verb} ${race}:<br />` + parseFloat(props[`${winner}`]).toFixed(2) + '%</b> <br />' 
            : 'Hover over a state');
            };
       
    
        //750,300,100,50,30
    function style(feature) {
        return {
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7,
        fillColor: getColor(feature.properties[`${winner}`])
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
        
        //var legend = L.control({position: 'bottomright'});
        
        //legend.onAdd = function (map) {
           
        
            //var div = L.DomUtil.create('div', 'info legend'),
                //grades = [-100, -20, -10, .001.toFixed(0), 10, 20, 30],
                //labels = [],
                //from, to;
        
            //for (var i = 0; i < grades.length; i++) {
                //from = grades[i];
                //to = grades[i + 1];
        
                //labels.push(
                    //'<i style="background:' + getColor(from + 1) + '"></i> ' +
                    //from + (to ? ' &ndash; ' + to : ' + '));
            //}
        
            //div.innerHTML = `<h4> ${new_category} Dem Margin</h4>` + labels.join('<br>');
            //return div;
        
        //}
        //if (legend instanceof L.Control) { map.removeControl(legend); }
        //if (info instanceof L.Control) { map.removeControl(info); }
        //legend.addTo(map);
        info.addTo(map);
        //if (legend instanceof L.Control) { map.removeControl(legend); }
        //if (info instanceof L.Control) { map.removeControl(info); }
        //if (geojson instanceof L.Control) { map.removeControl(info); }
        
        
    
    
    
    
    });

    
    
}
