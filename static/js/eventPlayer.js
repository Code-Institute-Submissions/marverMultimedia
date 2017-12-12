

if (window.location.pathname !== '/' && window.location.pathname !== '/events/'){
event_id = $('#event_id').val();
event_title = $('.webcast_title').val();
increaseAttendance('player',event_id,event_title);
}

$(document).ready(function(){

    $(document).on('click','input.star',function(e){
        $('#ratingSubmit').show();
        rating= e.currentTarget.value;
    });

    $('#ratingSubmit').click(function(e){
        userHasRated = sessionStorage.getItem('sessionId');
        if(userHasRated === null) {
            $.ajax({
                type: "POST",
                url: "/events/eventrating/",
                data: {
                    webcast_id: event_id,
                    rating: rating,
                    event_title:event_title
                },
                success: function (message) {
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

$('.playerForm').submit(function(e){

    e.preventDefault();

    var formType = '#' + e.currentTarget.getAttribute('id');

    var current =  e.currentTarget;

    var elementToRefresh = $(e.currentTarget).parents('.commentContainerClass').attr('id');

       $.ajax({
        type: 'POST',
        url: "/events/comment/",
        data: {
            form:$(formType + ' .formType').val(),
            name: $(formType + ' .name').val(),
            surname: $(formType + ' .surname').val(),
            email: $(formType + ' .email').val(),
            comment: $(formType + ' .comment').val(),
            webcast_id: $(formType + ' .webcast_id').val(),
            webcast_title: $(formType + ' .webcast_title').val(),
            date : date,
            issue_type :$(formType + ' .issue').val(),
            platform : navigator.platform,
            device : navigator.userAgent,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()

        },
        success: function (message) {

        $(current).next().css('color','red');
        $(current).next().html(message);
        setTimeout(function(){
            $(current).next().children('.supportFormMessage');
            $(elementToRefresh).modal('hide');
            $(elementToRefresh).load(' '+ elementToRefresh +'Inner')
            },3000)
        }
    })

});
