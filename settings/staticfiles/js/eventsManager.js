$(document).ready(function(){

//Datepicker function

     $('#dateInput').datepicker({
      altField: "#value",
      dateFormat: 'dd/mm/yy',
      altFormat: 'yy/mm/dd'
     });

     $('#ui-datepicker-div').css('display', 'none');

     $('#timepicker').timepicker({
      showMeridian: false
     });

});