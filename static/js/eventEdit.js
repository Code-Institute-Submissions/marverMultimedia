
//Webcast Creation/Edit Form Details
         //function in charge of returning the user to the event manager page in case they hit cancel in one of the
        // event creation/modification pages

     $(document).on('click', '#cancelbutton', function(e) {
      e.preventDefault();
      console.log('success');

      location.href = '/eventsmanager'
     });


    //webcastId variable has been initialized to 'undefined' on Webcast_creation form

        if (webcastId !== undefined) {
            var webcastStatusVerification = document.getElementById('id_webcast_status').value;
            console.log(webcastStatusVerification);
            document.getElementById('id_webcast_status').setAttribute('onchange', 'checkWebcastStatus(this.value)');
            var video = document.getElementById('div_id_webcast_video');
            if (webcastStatusVerification === "LIVE") {
                $(video).css('display', 'none');
            }
        }

        function checkWebcastStatus(status) {
        var video = document.getElementById('div_id_webcast_video');
            if (status === 'LIVE') {
                $(video).css('display','none');
            }
            else {
                $(video).css('display','block');
            }
        }


    //Webcast_edit.html page
    //Webcast Speaker Tab
    $(document).ready(function() {
        //mobile Menu Function
        $(document).on('click','.mobile-menu',function(e){
            console.log('done');
            $('ul.nav').slideToggle();
        });

     //Speakers Edit Section
     //speaker selection input animations
        $(document).on('click', '.speaker-selector-id-add',
            function(e) {
            e.preventDefault();
            console.log(e);
            $(this).parents('.single-speaker-container').addClass('speaker-selection-class');
            $(this).parents('.single-speaker-container').addClass('selected');
            $(this).css('display', 'none');
            $(this).next().css('display', 'block');
            console.log(this)
        });

        $(document).on('click', '.speaker-selector-id-remove',
         function(e) {
         e.preventDefault();
         $(this).parents('.single-speaker-container').removeClass('speaker-selection-class');
         $(this).parents('.single-speaker-container').removeClass('selected');
         $(this).css('display', 'none');
         $(this).prev().css('display', 'block');
         console.log(this)
     });

     //Ajax Function sending to web server view information about speakers assigned by the user to the Webcast

     function updateData(updateDataObject,data,elementMessage,origin) {
         console.log(data);
         $.ajax({
             type: 'POST',
             url: updateDataObject.url,
             data: data,
             success: function(message) {
                 if(origin === 'additionOnly'){
                     $(updateDataObject.modalContainer).modal('hide');
                    $(updateDataObject.containerToLoad).load(updateDataObject.innerContainer, function() {});
                    $(updateDataObject.modalContainer).load(updateDataObject.modalInner, function() {});
                     confirmationMessage('success',message,elementMessage)
                 }else {
                     $(updateDataObject.containerToLoad).load(updateDataObject.innerContainer, function () {
                     });
                     $(updateDataObject.modalContainer).load(updateDataObject.modalInner, function () {
                     });
                     $(updateDataObject.modalReload).load(updateDataObject.modalReloadInner);
                     confirmationMessage('success', message,elementMessage)
                 }
             },

             error: function(message){
                 confirmationMessage('error',message)
             }
         })
     }

     function confirmationMessage(status,message,elementMessage){
         if(status === 'error'){
             $(elementMessage).html(message);
                 $(elementMessage).css('color','red');
                 $(elementMessage).show();
                 setTimeout(function(){
                     $(elementMessage).hide();
                 },4000);
         }else{
              $(elementMessage).html(message);
                 $(elementMessage).css('color','green');
                 $(elementMessage).show();
                 setTimeout(function(){
                     $(elementMessage).hide();
                 },7000);
         }
     }



     //function that deletes the speakers selected and reloads the speaker container and modal window to update changes

     $(document).on('click', '.delete-checkbox:checkbox', function() {
         var deleteButtonAppear = document.getElementsByClassName('delete');
         if ($(this).parents('.single-speaker-container').hasClass('delete')) {
             $(this).parents('.single-speaker-container').removeClass('speaker-selection-class');
             $(this).parents('.single-speaker-container').removeClass('delete');
             if (deleteButtonAppear.length === 0) {
                 $('#delete-button').hide()
             }
         }
         else {
             $(this).parents('.single-speaker-container').addClass('speaker-selection-class');
             $(this).parents('.single-speaker-container').addClass('delete');
             $('#delete-button').show()
         }
     });

     // Function sending information with deleted speakers to web server asking to remove the speakers from the
     //database fields that associate the speaker to the webcast

     $(document).on('click', '#delete-button', function(e) {
         e.preventDefault();
         var getSelected = $('.delete').get();
         for (i = 0; i < getSelected.length; i++) {
             $.ajax({
                 type: 'POST',
                 url: "/eventsmanager/speakers_deletion",
                 data: {
                     speakers_id: getSelected[i].getAttribute('value'),
                     webcast_id: webcastId,
                     csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                 },
                 success: function(message) {
                     $('#speaker-update-messages').html(message);
                     $('#speaker-update-messages').css('color','green');
                     $('#speaker-update-messages').show();
                     setTimeout(function(){
                     $('#speaker-update-messages').hide();
                 },4000);
                 },
                 error: function(){
                     $('#speaker-update-messages').html(message);
                     $('#speaker-update-messages').css('color','red');
                     $('#speaker-update-messages').show();
                     setTimeout(function(){
                     $('#speaker-update-messages').hide();
                 },4000);
                 }
             });
             $('#delete-button').hide()
         }

         $('#myModal').load(" #modalDialog", function() {});

         $('.delete').hide()
     });

        //Function responsible for the speakers creation and communication with web server, timeouts take into account
        //communication times and process portion of page reloads#

        var speakerUpdateDataObj ={
            url : '/eventsmanager/speakers_addition',
            containerToLoad : '#speakers-container',
            innerContainer : ' #speakers-inner-container',
            modalContainer : '#myModal',
            modalInner:' #modalDialog',
            updateMessageElement : '#speaker-update-messages',
            modalReload: '#myModalSpeakerCreation',
            modalReloadInner : ' #modalDialogSpeakerCreation'
        };


     $(document).on('submit', '#SpeakerCreationForm', function(e) {
         var formdata = new FormData($('#SpeakerCreationForm').get(0));
         e.preventDefault();
         console.log(formdata);
         $.ajax({
             type: 'POST',
             url: "/eventsmanager/speakers_creation",
             data: formdata,
             success: function (message) {
                 $('#myModal').load(" #modalDialog", function () {
                 });
                 $('#myModalSpeakerCreation').modal('hide');
                 setTimeout(function () {
                     updateData(speakerUpdateDataObj,data={speakers_id:$('#speakersSelection').children('.single-speaker-container').last().attr('value'),
                         webcast_id : webcastId,csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()},'#speaker-update-messages','creation')
                 }, 2000);
             },
             error: function (message) {
                 $('#speaker-creation-error-modal').html(message);
                     $('#speaker-creation-error-modal').css('color','red');
                     $('#speaker-creation-error-modal').show();
                     setTimeout(function(){
                     $('#speaker-creation-error-modal').hide();
                 },4000);
             },
             processData: false,
             contentType: false
         })
     });

       //function reloading Speakers container and modal window to make them appear automatically once assigned to a webcast

     $(document).on('click', '#speakerSelectionSaveButton', function(e) {
         e.preventDefault();
         var data ={};
         var getSelected = $('.selected').get();
         getSelected.forEach(function(speaker){
             updateData(speakerUpdateDataObj,data= {speakers_id : speaker.getAttribute('value'),
                 webcast_id : webcastId,csrfmiddlewaretoken :$('input[name=csrfmiddlewaretoken]').val()},'#speaker-update-messages','additionOnly');
         });
     });


     //Assets Tab Functions

        var assetsUpdateDataObj ={
            url : '/eventsmanager/assets_addition',
            containerToLoad : '#assets-display-main-container',
            innerContainer : ' #assets-display-container',
            modalContainer : '#myModalAssets',
            modalInner:' #modalAssets',
            updateMessageElement : '#assets-update-messages',
            modalReload: '#myModalAssetUpload',
            modalReloadInner : ' #modalDialogAssetCreation'
        };

         //Function responsible for the asset creation and communication with web server, timeouts take into account
        //communication times and process portion of page reloads

     $(document).on('submit', '#AssetCreationForm', function(e) {
         var formdata = new FormData($('#AssetCreationForm').get(0));
         var data = {};
         e.preventDefault();
         console.log(formdata);
         $.ajax({
             type: 'POST',
             url: "/eventsmanager/asset_creation",
             data: formdata,
             success: function() {
                 $('#myModalAssets').load(" #modalAssets", function() {});
                 $('#myModalAssetUpload').modal('hide');
                 setTimeout(function () {
                 updateData(assetsUpdateDataObj, data={assets_id:$('#assetsSelection').children('.modal-asset-container').last().attr('value'),
                     webcast_id : webcastId,csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()},'#assets-update-messages','creation')
             },2000)},
             processData: false,
             contentType: false
         });
     });


      $(document).on('click', '#assetsSelectionSaveButton',
         function(e) {
             e.preventDefault();
             var data = {};
             var getSelected = $('.asset-selected').get();
             for (i = 0; i < getSelected.length; i++) {
                 updateData(assetsUpdateDataObj, data = {
                     assets_id: getSelected[i].getAttribute('value'),
                     webcast_id: webcastId,
                     csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                 },'#assets-update-messages', 'additionOnly')
             }
         });

//Function responsible for the addition of the classes selectors for the addition of speakers to the event in the speakers modal window
     $(document).on('click', '.asset-selector-id-add',
         function(e) {
         e.preventDefault();
         console.log(e);
         $(this).parents('.modal-asset-container').addClass('speaker-selection-class');
         $(this).parents('.modal-asset-container').addClass('asset-selected');
         $(this).css('display', 'none');
         $(this).next().css('display', 'block');
         console.log(this)
     });

     //function responsible for the removal of the classes selectors for the addition of speakers to the event in the speakers modal window
     $(document).on('click', '.asset-selector-id-remove',
         function(e) {
         e.preventDefault();
         $(this).parents('.modal-asset-container').removeClass('speaker-selection-class');
         $(this).parents('.modal-asset-container').removeClass('asset-selected');
         $(this).css('display', 'none');
         $(this).prev().css('display', 'block');
         console.log(this)
     });


     //function responsible for activating/deactivating the assets delete checkbox

     $(document).on('click', '.asset-delete-checkbox:checkbox', function() {
      var deleteButtonAppear = document.getElementsByClassName('asset-delete');
      console.log(deleteButtonAppear);

      if ($(this).parents('.assets-inner-container').hasClass('asset-delete')) {
          $(this).parents('.assets-inner-container').removeClass('speaker-selection-class');
          $(this).parents('.assets-inner-container').removeClass('asset-delete');

          if (deleteButtonAppear.length === 0) {

              $('#asset-delete-button').hide()
          }
      }
      else {

          $(this).parents('.assets-inner-container').addClass('speaker-selection-class');
          $(this).parents('.assets-inner-container').addClass('asset-delete');
          $('#asset-delete-button').show()
      }
     });

     $(document).on('click', '#asset-delete-button', function(e) {
      e.preventDefault();
      var getSelected = $('.asset-delete').get();
      for (i = 0; i < getSelected.length; i++) {
       $.ajax({
        type: 'POST',
        url: "/eventsmanager/assets_deletion",
        data: {
         assets_id: getSelected[i].getAttribute('value'),
         webcast_id: webcastId,
         csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },

        success: function(message) {
         confirmationMessage('success',message,'#assets-update-messages-deletion');
        },
        error: function(message) {
         confirmationMessage('error',message,'#assets-update-messages-deletion');
        }

       });
       $('#asset-delete-button').hide();
      }

      $('#myModalAssets').load(" #modalAssets", function() {});

      $('.asset-delete').hide()
     });

     //Agenda Create/Save/Edit

     checkAgendaStatus = $('#agenda-points-main-list > li');

     //set initially and maintain agenda points indexes in ordinal format, even when one of them is deleted
        function setAgendaIndexes() {
            listPointsCounter = $('#agenda-points-main-list > li');
            for (i = 0; i < listPointsCounter.length; i++) {
                listPointsCounter[i].childNodes[1].innerHTML = 'Agenda Point' + ' ' + (i + 1);
            }
        }
        setAgendaIndexes();


     $(document).on('click', '.btn-add',
         function(e) {
         checkPointsCounter = $('#agenda-points-main-list > li');
         //limit agenda to 15 points
             if (checkPointsCounter.length <= 14) {
                 if ($(this).prev('input').val() !== "") {
                     e.preventDefault();
                     var newField = $('.agenda-list-point-add').clone(false);
                     $(this).prev('input').replaceWith('<p style="width:50%;margin-right:5px; margin-top:5px; padding-left:10px;" ' +
                         'class="agenda-point-paragraph" title="Please click on the text to edit the agenda">' + $(this).prev('input').val() + '</p>');
                     $(this).addClass('btn-danger btn-remove');
                     $(this).removeClass('btn-success btn-add');
                     $(this).html('Remove');
                     $('#agenda-points-main-list').append(newField);
                     newField.prev('li').removeClass('agenda-list-point-add').addClass('agenda-list-point-remove');
                     $('#agenda-points-main-list > li:last-child').children('input').val('');
                     setAgendaIndexes();
                 }
                 else {
                     return false
                 }
             }
             else {
                 return false;
             }

     }).on('click', '.btn-remove',
         function(e) {
         $(this).parents('.agenda-list-point-remove').remove();
         setAgendaIndexes();
         e.preventDefault();
         return false;
     });

     //Function responsbile for collecting values from Agenda form, converting to Json and send to web server

     $(document).on('click', '#agendaSaveButton',
      function(e) {

       e.preventDefault();

       collectInputElements = document.getElementById('agenda-points-main-list').getElementsByTagName('input');
       collectPElements = document.getElementById('agenda-points-main-list').getElementsByTagName('p');
       for (i = 0; i < collectPElements; i++) {

        collectPElements[i].value(collectPElements[i].innerHTML)
       }

       collectAllElements = $('#agenda-points-main-list > li');
       agendaArray = [];
       for (i = 0; i < collectAllElements.length; i++) {

        if ($(collectAllElements[i]).find('p').length !== 0) {

         if ($(collectAllElements[i]).find('p')[0].innerHTML !== "") {

          agendaArray.push($(collectAllElements[i]).find('p')[0].innerHTML);

          console.log($(collectAllElements[i]).find('p').length);
         }

        } else {
         if ($(collectAllElements[i]).find('input')[0].value !== "") {
             agendaArray.push($(collectAllElements[i]).find('input')[0].value);
             console.log('I am an input');
         }
        }
       }

       agenda = JSON.stringify(agendaArray);

       console.log(agenda);

       $.ajax({
        type: 'POST',
        url: "/agenda",
        data: {
         'agenda': agenda,
         'webcast_id': webcastId,
         'agenda_id': agenda_id,
         csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(message) {
            confirmationMessage('success',message,'#agenda-update-messages')
        },
            error: function(message) {
            confirmationMessage('error',message,'#agenda-update-messages')
            }
       });
      });

     $(document).on('click', '.agenda-point-paragraph',
      function() {
       $(this).replaceWith('<input class="form-control agenda" value ="' + $(this).html() + '" name="fields[]" type="text" ' +
        'placeholder="Type Agenda Point Here.." autofocus style="width:50%;margin-right:5px" />');
      });



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

     //Function responsible to show the speaker picture uploaded in memory via the input element in the speaker creation modal
     function readUrl(input) {
      if (input.files && input.files[0]) {
       var readFile = new FileReader();

       readFile.onload = function(e) {
        $('#speaker-image-preview').attr('src', e.target.result);
       };

       readFile.readAsDataURL(input.files[0])
      }

     }
     $('#id_speaker_pic_url').change(function() {
      readUrl(this);
     });


     //function in charge of capturing the data from the canvas and send them in a 64 bit format to Python in order to
        //create a JPG file and upload to the S3 server

      var _VIDEO = document.querySelector('#video-element'),
          _CANVAS = document.querySelector('#canvas-element'),
          _CANVAS_CTX = _CANVAS.getContext("2d");

        _CANVAS.width = _VIDEO.videoWidth;
        _CANVAS.height = _VIDEO.videoHeight;

      document.querySelector('.file-input').addEventListener('change', function() {
          console.log('change is done');
          videoLink = document.querySelector('.file-link').getAttribute('href');
          console.log(videoLink);
          source = document.createElement('source');
          document.querySelector('#video-element').appendChild(source);
          document.querySelector('#video-element source').setAttribute('src', URL.createObjectURL(document.querySelector(".file-input").files[0]));
     });

      _VIDEO.addEventListener('loadedmetadata', function() {
          _CANVAS.width = _VIDEO.videoWidth;
          _CANVAS.height = _VIDEO.videoHeight;
          _VIDEO.currentTime = 2;
     });

      $(document).on('click','#download-link', function(e) {

          e.preventDefault();

          _CANVAS_CTX.drawImage(_VIDEO, 0, 0, _VIDEO.videoWidth, _VIDEO.videoHeight);

          var dataURL = _CANVAS.toDataURL('image/jpeg',0.7);

           $.ajax({
               type: 'POST',
               url: "/thumbnail_upload",
               data: {
                   webcast_image : dataURL,
                   webcast_id : webcastId

               },
               success: function (message) {
                   $('#thumbnail-success-message').show();
                   $('#thumbnail-success-message').html(message);

                   setTimeout(function(){
                       $('#thumbnail-success-message').hide();
                   },5000)
               },
               error: function (message) {
                   $('#thumbnail-success-message').show();
                   $('#thumbnail-success-message').html(message);
                   setTimeout(function(){
                       $('#thumbnail-success-message').hide();
                   },5000)
               }
           });
      });

    //Chapter Create/Save/Edit

     checkAgendaStatus = $('#chapters-points-main-list > li');

     //set initially and maintain agenda points indexes in ordinal format, even when one of them is deleted
        function setChaptersIndexes() {
            listPointsCounter = $('#chapters-points-main-list > li');
            for (i = 0; i < listPointsCounter.length; i++) {
                listPointsCounter[i].childNodes[1].innerHTML = 'Chapter' + ' ' + (i + 1);
            }
        }
        setChaptersIndexes();


     $(document).on('click', '.chapter-btn-add',
         function(e) {
         var video = document.getElementById('video-element');
         checkPointsCounter = $('#chapters-points-main-list > li');
         //limit agenda to 15 points
             if (checkPointsCounter.length <= 14) {
                 if (video.currentTime !== 0 && $(this).prev('input').val()!== "") {
                     $('#chapters-update-messages').hide();
                     e.preventDefault();
                     _CANVAS_CTX.drawImage(_VIDEO, 0, 0, _VIDEO.videoWidth, _VIDEO.videoHeight);
                     var dataURL = _CANVAS.toDataURL('image/jpeg',0.30);
                     var minutes = Math.floor(video.currentTime / 60);
                     var seconds = Math.floor(video.currentTime - minutes *60);
                     var newField = $('.chapter-list-point-add').clone(false);
                     var imageContainer = document.createElement('img');

                     if (seconds < 10){
                       timeString = " " +  minutes + ":" + "0" + seconds;
                     } else{
                        timeString = "" +  minutes + ":" + seconds;
                     }


                     $(imageContainer).css('width','200px');
                     $(imageContainer).css('height','115px');
                     $(imageContainer).attr('src',dataURL);
                     $(imageContainer).addClass('chapterThumbnailContainer');
                     $(this).parent('.chapter-list-point-add').children('.chapter-title').val($(this).prev('input').val());
                     $(this).parent('.chapter-list-point-add').children('.chapter-time').val(Math.floor(video.currentTime));
                     $(this).parent('.chapter-list-point-add').children('.chapter-time-readable').val(timeString);
                     $(this).prev('input').replaceWith('<p style="width:50%;margin-right:5px; margin-top:5px; padding-left:10px;" ' +
                         'class="chapter-point-paragraph">' + "Time:" + timeString + '<br>' +  'Chapter Title:'+ $(this).prev('input').val() + '</p>');

                     $(this).addClass('btn-danger chapter-btn-remove');
                     $(this).removeClass('btn-success chapter-btn-add');
                     $(this).html('Remove');
                     $(this).parent('.chapter-list-point-add').append(imageContainer);
                     $('#chapters-points-main-list').append(newField);
                     newField.prev('li').removeClass('chapter-list-point-add').addClass('chapter-list-point-remove');
                     $('#chapters-points-main-list > li:last-child').children('input').val('');
                     setChaptersIndexes();
                 }
                 else {
                     e.preventDefault();
                     console.log('error');
                     $('#chapters-update-messages').show();
                     $('#chapters-update-messages').html('Please insert a title');
                     return false
                 }
             }
             else {
                 return false;
             }

     }).on('click', '.chapter-btn-remove',
         function(e) {
         e.preventDefault();
         $(this).parents('.chapter-list-point-remove').remove();
         setChaptersIndexes();
         return false;
     });

     //Function responsbile for collecting values from Agenda form, converting to Json and send to web server

     $(document).on('click', '#chapterSaveButton',
      function(e) {



       e.preventDefault();

       collectTitleElements = $('.chapter-title');
       collectTimeElements = $('.chapter-time');
       collectThumbnails = $('.chapterThumbnailContainer');
       collectTimeReadableElements = $('.chapter-time-readable');

        var chapterObject = {};
        var chapterArray = [];
        var thumbnailsArray = [];

        for(i=0; i<collectTitleElements.length;i++){
            if(collectTitleElements[i].value !== ""){
            chapterObject = {
                'time' : collectTimeElements[i].value,
                'title' : collectTitleElements[i].value,
                'imgUrl' :  'https://elasticbeanstalk-eu-west-2-932524864295.s3.amazonaws.com/media/webcast_'+ webcastId +'/ChapterThumbnail_'+i+'.png',
                'timeReadable' : collectTimeReadableElements[i].value
            };
            chapterArray.push(chapterObject);
            }
        }

        for(i=0;i<collectThumbnails.length;i++){
            thumbnailsArray.push($(collectThumbnails[i]).attr('src'))
        }
        console.log(chapterArray);
       chapters = JSON.stringify(chapterArray);
       thumbnails = JSON.stringify(thumbnailsArray);
       $.ajax({
        type: 'POST',
        url: "/chapters",
        data: {
         'chapters': chapters,
         'webcast_id': webcastId,
         'chapters_id': chapters_id,
        'thumbnailsImg' : thumbnails,
         csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(message) {
            confirmationMessage('success',message,'#chapters-update-messages')
        },
            error: function(message) {
            confirmationMessage('error',message,'#chapters-update-messages')
            }
       });
      });



    });