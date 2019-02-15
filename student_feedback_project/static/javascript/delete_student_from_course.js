$('.delete-icon').click(function(e) {
  var result = confirm("Want to delete?");
  if(result){
//send request to delete relationship:
//send student_name and course_code (strings)

  var host = location.protocol + "//" + window.location.host;
  const Url = host + "/StudentCourseRelDestroy/" + this.id;
  var csrftoken = getCookie("csrftoken");
  function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
  });
  $.ajax({
      url: Url,
      data: {},
      type: 'DELETE',
      contentType: 'application/json',
      success: function(result) {
        location.reload();
      },
  });
  }
});

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
