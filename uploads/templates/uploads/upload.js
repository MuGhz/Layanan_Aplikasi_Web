interval = null;

function openProgressBar() {
/* generate random progress-id */
uuid = "";
for (i = 0; i < 32; i++) {
 uuid += Math.floor(Math.random() * 16).toString(16);
}
/* patch the form-action tag to include the progress-id */
document.getElementById("upload").action="/uploads/test?X-Progress-ID=" + uuid;

/* call the progress-updater every 1000ms */
interval = window.setInterval(
  function () {
    fetch(uuid);
  },
  1000
);
}

function fetch(uuid) {
console.log('fetch uuid');
req = new XMLHttpRequest();
req.open("GET", "/progress", false);
req.setRequestHeader("X-Progress-ID", uuid);
req.onreadystatechange = function () {
console.log('onready state change');
 if (req.readyState == 4) {
  if (req.status == 200) {
   /* poor-man JSON parser */
   var upload = eval(req.responseText);
   console.log(upload);
   document.getElementById('tp').innerHTML = upload.state;

   /* change the width if the inner progress-bar */
   if (upload.state == 'done' || upload.state == 'uploading') {
    bar = document.getElementById('progressbar');
    w = 400 * upload.received / upload.size;
    console.log(w);
    bar.style.width = w + 'px';
   }
   /* we are done, stop the interval */
   if (upload.state == 'done') {
    window.clearTimeout(interval);
   }
  }
 }
}
req.send(null);
}
