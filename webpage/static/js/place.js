var autocomplete = new google.maps.places.Autocomplete(document.getElementById('address-input'));
function init() {
	var options = {
		types: ['(cities)']
	};
 
	var input = document.getElementById('address-input');
	var autocomplete = new google.maps.places.Autocomplete(input, options);
}
google.maps.event.addDomListener(window, 'load', init);