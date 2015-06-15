// SEMANTIC JS
$('.ui.menu .item').tab({
  onTabLoad: function(){
    map_search.invalidateSize(); // update maps when changing tabs so they don't display blank parts.
    map_view.invalidateSize();
  },
});
$('.dropdown').dropdown();
$('.ui.checkbox').checkbox();
// END OF SEMANTIC JS

// MONTHPICKERS JS
$('#from_month_picker').MonthPicker({ ShowIcon: false });
$('#to_month_picker').MonthPicker({ ShowIcon: false });
// END OF MONTHPICKER JS

// GENERAL INFORMATION
    // from json file (file has to be on server, because of javascript limitations
    // (security limitation, so that javascript can't open local files)
    // recomended implementation: open a command shell and write (tested on ubuntu):
    // python3 -m http.server
    // so you can access to the page in htpp://localhost:8000/home.html
$.getJSON('processed_data/info.json', function(data) {
  for (var key in data){
    $('#' + key).text(data[key]);
  }
});
// END OF GENERAL INFORMATION


// FIRST MAP
var tiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors.'
  }),
  latlng = L.latLng(10.5, -10.5);

var map_view = L.map('map_view', {center: latlng, zoom: 2, layers: [tiles]});
var markers = L.markerClusterGroup();

for (var i = 0; i < locations.length; i++) {
  var coordinates = locations[i];
  var marker = L.marker(new L.LatLng(coordinates[1], coordinates[2]));
  marker.bindPopup("<br>", {minWidth: 200});
  markers.addLayer(marker);
}
map_view.addLayer(markers);
// END OF FIRST MAP


// IMAGES FROM API TO MARKERS
function imagize_popup(marker) {
  var coordinates = [0, marker.getLatLng().lat, marker.getLatLng().lng]
  $.ajax({
    async: false,
    url: 'http://commons.wikimedia.org/w/api.php?format=json&action=query&generator=geosearch&ggsprimary=all&ggsnamespace=6&ggsradius=2000&ggscoord=' + coordinates[1] + '|' + coordinates[2] + '&ggslimit=1&prop=imageinfo&iilimit=1&iiprop=url&iiurlwidth=200&iiurlheight=200',
    type: 'GET',
    dataType: "jsonp",
    success: function(data){
      if (data['query']){
        var title = data.query.pages[Object.keys(data.query.pages)[0]].title;
        title = title.substring(5, title.length - 4);
        var url = data.query.pages[Object.keys(data.query.pages)[0]]['imageinfo'][0]['thumburl'];
        marker.setPopupContent("<img src='" + url + "'/>" + "<br>" + title, {minWidth: 200});
        marker.getPopup().update();
      }
      else {
        marker.setPopupContent("Imagen no disponible en estas coordenadas, pruebe con otro marcador.");
      }
    }
  });
}
  // onclick event, trigger function to get and display an image
map_view.on('popupopen', function(e){
  var marker = e.popup._source;
  imagize_popup(marker);
});
  // end of onclick event
// END OF IMAGES

// with data obtained from a json, adds users to the dropdown, so they can be searched (2nd tab)
$.getJSON('processed_data/input3.json', function(data) {
  for (var i in data['usuarios']){
    var user = data['usuarios'][i];
    $('.dropdown .menu').append('<div class="item" data-value="' + i + '">' + user['id'] + '</div>');
  }
});

// validates that a user is selected
$('.ui.form').form({
    user: {
      identifier  : 'user',
      rules: [
        {
          type   : 'empty',
          prompt : 'Por favor seleccione un usuario'
        }
      ]
    }
  }, {
    inline: true,
    onSuccess: validate
  });

// validates with regex, that optional dates are valid
function validate() {
  $('#no_checkins_error').hide();
  $('.paddingless').addClass('loading');
  $('#from_error').hide();
  $('#to_error').hide();
  var form_data = $('.ui.form').serializeArray();
  var amount = form_data.length;
  var re = /^(1[0-2]|0[1-9])\/(\d{4})$/i;
  var to_date_str = form_data[amount - 1].value
  var from_date_str = form_data[amount - 2].value
  var error_text = 'Por favor introduzca una fecha válida de formato "mm/yyyy"';
  from_valid = re.test(from_date_str)
  to_valid = re.test(to_date_str)
  if (from_date_str != '' && to_date_str != '' && from_valid && to_valid){
    filter(form_data);
  }
  else if (from_date_str != '' && from_valid && to_date_str == ''){
    filter(form_data);
  }
  else if (to_date_str != '' && to_valid && from_date_str == ''){
    filter(form_data);
  }
  if (from_date_str != '' && !from_valid){
    $('#from_error').show().text(error_text);
  }
  if (to_date_str != '' && !to_valid){
    $('#to_error').show().text(error_text);
  }
  else {
    filter(form_data);
  }
}

// SECOND MAP
var tiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors.'
  }),
  latlng = L.latLng(10.5, -10.5);

var map_search = L.map('map_search', {center: latlng, zoom: 2, layers: [tiles]});

// END OF SECOND MAP

// this is the function called if the form is valid
// gets info from json file, creates markers between the given date
// adds markers from friends if required, adjusts the map to boundries,
// and it creates routes, with an arrow dinamically showing the path.
function filter(array) {
  // var bounds_array = []
  var path_array = []
  map_search.eachLayer(function (layer){
    if(layer != tiles){
      map_search.removeLayer(layer);
    }
  });
  $.getJSON('processed_data/input3.json', function(data) {
    var to_date = new Date();
    var from_date = new Date(1);
    var markers = L.layerGroup();
    var user = data['usuarios'][array[0]['value']];
    var greenIcon = L.icon({
      iconUrl: 'static/icons/marker-icon_green.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [-3, -76],
      shadowUrl: 'static/icons/marker-shadow.png',
      shadowSize: [41, 41],
      shadowAnchor: [12, 41]
    });
    if (array[array.length - 2]['value'] != ''){
      var date_array = array[array.length - 2]['value'].split('/');
      var date_str = date_array[0] + '/01/' + date_array[1];
      var from_date = new Date(date_str);
      // console.log('f', from_date);
    }
    if (array[array.length - 1]['value'] != ''){
      var date_array = array[array.length - 1]['value'].split('/');
      var to_date = new Date(date_array[1], date_array[0]);
      // console.log('t', to_date);
    }
    for(var i in user['check-ins']){
      var checkin = user['check-ins'][i];
      var latlng = new L.LatLng(checkin['latitude'], checkin['longitude']);
      marker = L.marker(latlng);//.addTo(map_search);
      var checkin_date = new Date(checkin['time']);
      if (from_date <= checkin_date && checkin_date <= to_date){
        // console.log('a', checkin_date);
        // bounds_array.push(latlng);
        path_array.push(latlng);
        markers.addLayer(marker);
      }
    }
    map_search.addLayer(markers);
    if (array[1]['name'] == 'friends'){
      var friends = user['amigos']
      for (var i in user['amigos']){
        var friend_checkins = user['amigos'][i]['check-ins']
        for (var j in friend_checkins){
          var f_checkin = friend_checkins[j]
          var f_latlng = new L.LatLng(f_checkin['latitude'], f_checkin['longitude']);
          var friend_date = new Date(f_checkin['time']);
          if (from_date <= friend_date && friend_date <= to_date){
            // console.log('fr', friend_date);
            // bounds_array.push(f_latlng);
            f_marker = L.marker(f_latlng, {icon : greenIcon}).addTo(map_search);
          }
        }
      }
    }
    if (path_array.length > 0){
      var bounds_item = new L.LatLngBounds(path_array);
      map_search.fitBounds(bounds_item);
    }
    else {
      $('#no_checkins_error').show().text('No hay checkins para ese usuario en el intervalo escogido');
    }
    $('.paddingless').removeClass('loading');
    if (array[array.length - 3]['name'] == 'paths'){
      var polyline = L.polyline(path_array, {color: 'red', opacity: 0.3}).addTo(map_search);
      var arrowHead = L.polylineDecorator(polyline, {opacity: 0.15}).addTo(map_search);
      var arrowOffset = 0;
      var anim = window.setInterval(function() {
          arrowHead.setPatterns([
            {offset: arrowOffset+'%', repeat: 0, symbol: L.Symbol.arrowHead({pixelSize: 15, polygon: false, pathOptions: {stroke: true}})}
          ])
          if(++arrowOffset > 100)
            arrowOffset = 0;
        }, 500);
    }
  });
}
