var apiKey = "pk.eyJ1IjoiZGFydGFuaW9uIiwiYSI6ImNqbThjbHFqczNrcjkzcG10cHpoaWF4aWUifQ.GwBz1hO0sY2QE8bXq9pSRg";
var mapboxAccessToken = apiKey;
var graymap = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + mapboxAccessToken, {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox/light-v10"
});
//L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + mapboxAccessToken, {
    //id: 'mapbox/light-v9',
    //attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",

var satellite = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + mapboxAccessToken, {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox/satellite-streets-v11"
});

var outdoors = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + mapboxAccessToken, {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox/outdoors-v11"
});

var map = L.map("map", {
    center: [
      40.7, -94.5
    ],
    zoom: 3,
    layers: [graymap, satellite, outdoors]
  });
var election_2016 = new L.LayerGroup();
var election_2018 = new L.LayerGroup();
var election_2020 = new L.LayerGroup();
var baseMaps = {
    Satellite: satellite,
    Graymap: graymap,
    Outdoors: outdoors
  };
var overlays = {
    "Election 2016": election_2016,
    "Election 2018" : election_2018,
    "Election 2020" : election_2020
  };
  
L
    .control
    .layers(baseMaps, overlays)
    .addTo(map);


d3.selectAll("#categories").on("change", menu);
function menu() { var selectedCategory = d3.select("#categories option:checked");
var category = selectedCategory.property("value");
console.log(geojson);
console.log(category);


if (category == 2018) {
    winner = "midterm_dem_vote";
    president = "Democratic Party";
    loser = "midterm_gop_vote";
    runner_up = "Republican Party";
    year = "midterm_margin";
    new_category = 2018;
    //query_url = "https://raw.githubusercontent.com/zachtspahr/zachtspahr.github.io/master/2018_districts_data.json"
} else if (category == 2020) {
    winner = "2020_dem_pct";
    president = "Democratic Party"
    loser = "2020_gop_pct";
    runner_up = "Republican Party"
    year = "2020_dem_margin";
    new_category = 2020;
    //query_url="https://raw.githubusercontent.com/zachtspahr/zachtspahr.github.io/master/2020_congressional_data.json"
  } else {
    winner = "2016_gop_house_pct";
    president = "Republican Party"
    loser = "2016_dem_house_pct";
    runner_up = "Democratic Party"
    year = "2016_dem_house_margin"
    new_category = 2016
    //query_url= "https://raw.githubusercontent.com/zachtspahr/zachtspahr.github.io/master/2016_districts_data.json";
    //removeFeature(L.geoJson(),id);
    //map.clearLayers();
  }}