
if (window.location.pathname === '/' || window.location.pathname === '/events/') {
    increaseAttendance();
}
$(document).ready(function(){

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

    var url = 'order?option=' + action;
    var site = url + " #events-inner-container";
    $.get('/events/order?option=' + action, function(){
        $('#events-container').load(site, function() {
            $('#events-container').show();
            $('.empty-month-message').css('display','none');
        })

    }).fail(function(message){
        $('#events-container').hide();
        $('#events-container').load(site, function() {});
        $('.empty-month-message h3').html(message.responseText);
        $('.empty-month-message').css('display','block');

    })

});

    $('#search-button').click(function(e) {

        if ($('#search-input').val()=== ''){
            return null
        }
        else{
        e.preventDefault();

        string = $('#search-input').val();
        var url = 'searchevents?search=' + string;
        site = url + " #events-inner-container";
        $.get('/events/searchevents?search=' + string, function () {
            $('#events-container').load(site, function () {
                $('#events-container').show();
                $('.empty-month-message').css('display', 'none');
            })
        }).fail(function (message) {
            $('#events-container').hide();
            $('#events-container').load(site, function () {
            });
            $('.empty-month-message h3').html(message.responseText);
            $('.empty-month-message').css('display', 'block')
        })
            }
    });

});





