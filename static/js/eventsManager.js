$(document).ready(function(){

//Datepicker function

     /*$('#dateInput').datepicker({
      altField: "#value",
      dateFormat: 'dd/mm/yy',
      altFormat: 'yy/mm/dd'
     });

     $('#ui-datepicker-div').css('display', 'none');

     $('#timepicker').timepicker({
      showMeridian: false
     });*/

     $(document).on('click','.reorder',function(e){
         e.preventDefault();
         data = e.target.text;
         split = data.split(' ');
         var action = 0;
         var months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
         for(i=0;i<months.length;i++){
             if (split[0] === months[i]){
                 action = i +1;
             }
         }

         var userId = $('.userid').attr('id');

         var url = '/orderevents?option=' + action + '&pk=' + userId;
         var site = url + " #events-manager-events-inner-container";
         $.get('/orderevents?option=' + action + '&pk=' + userId, function(){
             $('#events-manager-events-container').load(site, function() {
            $('#events-manager-events-container').show();
            $('.empty-month-message').css('display','none');
         })

         }).fail(function(message){
             $('#events-manager-events-container').hide();
             $('#events-manager-events-container').load(site, function() {});
             $('.empty-month-message h3').html(message.responseText);
             $('.empty-month-message').css('display','block')
         })

     });

     $('#search-button').click(function(e) {

         var userId = $('.userid').attr('id');

         e.preventDefault();
         string = $('#search-input').val();
         var url = '/searchevents?search=' + string + '&pk=' + userId;
         site = url + " #events-manager-events-inner-container";
         $.get(url, function () {
             $('#events-manager-events-container').load(site, function() {
                 $('#events-manager-events-container').show();
                 $('.empty-month-message').css('display','none');
             })
         }).fail(function (message) {
             $('#events-manager-events-container').hide();
             $('#events-manager-events-container').load(site, function () {
             });
             $('.empty-month-message h3').html(message.responseText);
             $('.empty-month-message').css('display', 'block')
         })
     });

});