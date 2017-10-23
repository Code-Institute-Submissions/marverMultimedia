 /* Home Page Carousel Function */

    function carousell(element, side, node, webcasts) {
        element.preventDefault();
        var getNumberOfImages = document.getElementById(node).getElementsByClassName(webcasts);
        console.log(getNumberOfImages);
        var imagesArrayLength = getNumberOfImages.length - 1;
        var pos = 570;
        var carousel = document.getElementById(node);
        var right;
        var left;

     //when user either hits the right carousel chevron or the left one, an action will take place as per below

        if (side === 'left') {
         right = setInterval(moveright, 2);
         setTimeout(reshuffleImages, 1000);
        }
        else if (side === 'right') {
         left = setInterval(moveleft, 2);
         setTimeout(reshuffleImages, 1000);
        }

     //Functions call when the chevron is hit and the animation starts, the top picture is being "cloned" and attached at the back of
     // the images queue, whilst the instance currently at the top is being removed

         function reshuffleImages() {
             var topImage = getNumberOfImages[imagesArrayLength].innerHTML;
             var new_image = document.createElement('div');
             new_image.innerHTML = topImage;
             new_image.setAttribute('class', webcasts);
             document.getElementById(node).insertBefore(new_image, carousel.childNodes[0]);
             document.getElementById(node).removeChild(getNumberOfImages[imagesArrayLength + 1]);
         }


         function moveleft() {
             if (pos === -570) {
                 clearInterval(left);
             }
             else {
                 pos -= 10;
                 $('.' + webcasts).last().css('left', pos + "px");
             }
         }

         function moveright() {
             if (pos === 1540) {
                 clearInterval(right);
             }
             else {
                 pos += 10;
                 $('.' + webcasts).last().css('left', pos + "px");
             }
         }
    }
 /*Player page hidden menu, makes the boxes under the video section appear/disappear */


    function toggleInfoAppear(button) {

        var whatBox = button.id;
        var whatBoxSlice = "#" + whatBox.slice(6, whatBox.length).toLowerCase();
        var isActive = $(whatBoxSlice).css('opacity');
        if (isActive >= 1) {
            setInterval(makeBoxDisappear, 50);
        }
        else if (isActive <= 0) {

            setInterval(makeBoxAppear, 50);
        }
        var op = 0;
        function makeBoxAppear() {
            if (op >= 1) {
                clearInterval(makeBoxAppear);
            }
            else {
                op += 0.1;
                $(whatBoxSlice).css('display', 'block');
                $(whatBoxSlice).css('opacity', op);
            }
        }

        var opD = 1;
        function makeBoxDisappear() {
            if (opD < 0) {
                clearInterval(makeBoxDisappear);
            }
            else {
                opD -= 0.1;
                $(whatBoxSlice).css('opacity', opD);
                setTimeout(function() {
                    $(whatBoxSlice).css('display', 'none');
                }, 500);
            }
        }
    }

    $(function(){

        $('#register-form').submit(function(event){
            event.preventDefault();

            var form = this;
            var card = {
                number:   $("#id_creditcardnumber").val(),
                expMonth: $("#id_expiry_month").val(),
                expYear:  $("#id_expiry_year").val(),
                cvc:      $("#id_cvv").val()
            };

            console.log(card.number);

            $('#validate_card_btn').attr('disabled',true);
            Stripe.createToken(card, function(status,response){
                if(status === 200){
                    console.log(response);
                    $('#credit-card-errors').hide();
                    $('#id_stripe_id').val(response.id);
                    form.submit();
                }
                else{
                   $("#stripe-error-message").text(response.error.message);
                   $("#credit-card-errors").show();
                   $("#validate_card_btn").attr("disabled", false);
                }

            });
            return false;
        })
    });

$(document).ready(function() {

    //mobile Menu Function
    $(document).on('click', '.mobile-menu', function (e) {
        console.log('done');
        $('ul.nav').slideToggle();
    });

    $(document).on('mouseover', '#dropdown-link',function(e){
         $('#dropdown-menu').slideDown();
    });
    $(document).on('mouseleave', '#dropdown-link',function(e){
         $('#dropdown-menu').slideUp();
    })

});