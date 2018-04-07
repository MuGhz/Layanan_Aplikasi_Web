jQuery.nginxUploadProgress = function(settings) {
 settings = jQuery.extend({
   interval: 2000,
   progress_bar_id: "progressbar",
   nginx_progress_url: "/progress"
 }, settings);


    $("#upload").submit(function() {
        $('#'+settings['progress_bar_id']).width('0%');

        // Create a new upload uuid and update ajaxSubmit url with it
        var uuid = "" + new Date().getTime() + Math.floor(Math.random()*100);
        var action = $('#upload').attr('action');
        var full_url = 'http://host21014.proxy.infralabs.cs.ui.ac.id/uploads/progress?X-Progress-ID='+uuid;
        var options = {
                url: full_url,
          beforeSubmit: function(formData, jqForm, options) {
           // TODO HERE!!! set the url (like above) every time we submit the form (so in this method...). Setting the form's action in the dom doesn't work because ajaxForm uses the url param above

           $('#error').hide();
           $('#uploader .desc').hide();
           $('#uploader').hide();
           $('#uploading').show();

           this.timer = setInterval(function() { jQuery.nginxUploadProgressFetch(this, settings['nginx_progress_url'], settings['progress_bar_id'], uuid) }, settings['interval']);
           return true;
         },
          complete: function(xhr, statusText)  {
                // alert(statusText);
                // for(x in xhr) {alert(x+':'+xhr[x])}
                // alert(xhr.data);
                // alert(xhr.getResponseHeader("content-type"));
                // alert(xhr.getResponseHeader("content-type"));
           data = eval("(" + xhr.responseText + ")");
           if (data.location) {
               window.location.href = data.location;
           } else {
clearInterval(this.timer);
               $('#uploader').show();
               $('#uploading').hide();
               $('#error').show();
               if (data.error == "NotValid") {
                   $('#error_not_valid').show();
               } else if (data.error == "FormatNotRecognised") {
                   $('#error_format_not_recognised').show();
               } else {
                   $('#error_unknown').show();
               }
           }
         },
          dataType: 'json'        // 'xml', 'script', or 'json' (expected server response type)
      };

        $(this).ajaxSubmit(options);
        return false;
    });
};

jQuery.nginxUploadProgress.inum = 0;

jQuery.nginxUploadProgressFetch = function(e, nginx_progress_url, progress_bar_id, uuid) {
 // window.console.log("fetcing progress for "+uuid)
 jQuery.nginxUploadProgress.inum++;

 $.ajax({
   type: "GET",
   url: nginx_progress_url,
   dataType: "json",
   beforeSend: function(xhr) {
     xhr.setRequestHeader("X-Progress-ID", uuid);
     // window.console.log("setting headers: "+uuid)
   },
   complete: function(xhr, statusText) {
     // window.console.log("complete!: "+statusText);
   },
   success: function(upload) {
     /* change the width if the inner progress-bar */
     if (upload.state == 'uploading') {
       bar = $('#'+progress_bar_id);
       w = Math.floor((upload.received / upload.size)*100);
       bar.width(w + '%');

       // Panda specific
       bar.show();

       // Update ETA
       eta_seconds = ((upload.size / upload.received) * jQuery.nginxUploadProgress.inum) - jQuery.nginxUploadProgress.inum;

       if (eta_seconds < 60) {
         eta_str = "under a minute"
       } else if (eta_seconds < (60*5)) {
         eta_str = "a few minutes"
       } else if (eta_seconds < (60*15)) {
         eta_str = "fifteen minutes"
       } else if (eta_seconds < (60*30)) {
         eta_str = "about half an hour"
       } else if (eta_seconds < (60*45)) {
         eta_str = "around 45 minutes"
       } else if (eta_seconds < (60*60)) {
         eta_str = "less than an hour"
       } else if (eta_seconds > (60*60)) {
         eta_str = "over an hour";
       } else if (eta_seconds > (60*60*2)) {
         eta_str = "a few hours";
       } else if (eta_seconds > (60*60*3)) {
         eta_str = "several hours";
       } else if (eta_seconds > (60*60*6)) {
         eta_str = "quite a long time... at least 6 hours";
       } else {
         eta_str = "";
       }

       $("#eta").html(eta_str);
     } else if (upload.state == 'error') {
       $('#uploader').show();
       $('#uploading').hide();
       $('#error').show();
       if (upload.status == 413) {
         $('#error_too_large').show();
       } else {
         $('#error_unknown').show();
       }
     }
   }
 });
};
