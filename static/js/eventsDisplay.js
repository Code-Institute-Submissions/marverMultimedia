
if (window.location.pathname === '/' || window.location.pathname === '/events/') {
console.log(window.location);
    increaseAttendace();
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

    var url = 'orderevents/option_' + action;
    var site = url + " #events-inner-container";
    $.get('/events/orderevents/option_' + action, function(){
        $('#events-container').load(site, function() {
            $('#events-container').show();
            $('.empty-month-message').css('display','none');
        })

    }).fail(function(message){
        $('#events-container').hide();
        $('#events-container').load(site, function() {});
        $('.empty-month-message h3').html(message.responseText);
        $('.empty-month-message').css('display','block')

    })

});

    $('#search-button').click(function(e) {

        e.preventDefault();

        string = $('#search-input').val();
        var url = 'searchevents/search_' + string;
        site = url + " #events-inner-container";
        $.get('/events/searchevents/search_' + string, function () {
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
    });

    $(document).on('click','input.star',function(e){
        $('#ratingSubmit').show();
        rating= e.currentTarget.value;
        console.log(rating);
    });

    $('#ratingSubmit').click(function(e){
        userHasRated = sessionStorage.getItem('sessionId');
        console.log(userHasRated);
        console.log(rating);
        if(userHasRated === null) {
            $.ajax({
                type: "POST",
                url: "/events/eventrating/",
                data: {
                    webcast_id: webcastId,
                    rating: rating
                },
                success: function (message) {
                    console.log(message);
                    sessionStorage.setItem('sessionId',1);
                    $('#ratingSubmit').hide();
                    $('.rating-message').html(message);
                    setTimeout(function(){$('.rating-message').hide();},3000);
                }
            })
        }
        else{
            $('#ratingSubmit').hide();
            $('.rating-message').show().html("You have already voted for this session");
            setTimeout(function(){$('.rating-message').hide();},3000);
        }
    });

});





