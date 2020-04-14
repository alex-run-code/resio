// $(document).ready(function () {
//   $('select').niceSelect();
// });

var hospitals = [
  { value: 'Regina Maria', data: 'Regina Maria' },
  { value: 'Saint Joseph', data: 'Saint Joseph' }
];

$('#autocomplete').autocomplete({
  lookup: hospitals,
  onSelect: function (suggestion) {
    // alert('You selected: ' + suggestion.value + ', ' + suggestion.data);
    this.value = suggestion.value;
  }
});
