// this is for Ajax CSRF_TOKEN ((((((  DO NOT CHANGE IT/ REMOVE  ))))))

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
  }
});

// END AJAX CSRF_TOKEN 

$(document).on('click', '.send_Mail', function () {

    var getMailValue = document.getElementById('GET_OTP').value;

    $.ajax({
        url: "",
        method: "post",
        data: {
              name: 'Send_code',
              email: getMailValue,
        },
        success: function(data){
              alert("Verifivation Code Sent Successfully!")
        }
    });
})