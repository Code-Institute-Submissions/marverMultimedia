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
