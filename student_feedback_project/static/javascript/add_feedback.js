var catborder = 'cat-border';
$('.cat-item').click(function(e) {
  // This is needed to ensure that only one category is selected at a time
  $('.cat-item').each(function(e) {
    if($(this).hasClass(catborder)){
      $(this).toggleClass(catborder);
    }
  });
  $(this).toggleClass(catborder);

  var cat_id = $(this).attr('id');
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
      url: "/category/"+cat_id+"/",
      data: {},
      type: 'GET',
      contentType: 'application/json',
      success: function(result) {
        // The difficulty with this was that the context dictionary cannot be accessed in this
        // separate javascript file. So call a method in the HTML template which retrieves data
        // And sends data back to file in method updateHtml()
        displayMessages(result,cat_id);
      },
  });
});

var messborder = "mess-border";
$('.messages').on('click','.mess-item',function() {
  // This is needed to ensure that only one message is selected at a time
  $('.mess-item').each(function() {
    if($(this).hasClass(messborder)){
      $(this).toggleClass(messborder);
    }
  });
  $(this).toggleClass(messborder);
});

$('#submit-fb-form').click(function(e) {

  var location = window.location.href;
  var student_id = location.split("/")[5];
  var course = location.split("/")[4];

  var cat_id = $('.cat-border').attr("id");
  var mess_id = $('.mess-border').attr("id");

  var points = $('#id_points').val();
  var optional_message = $('#id_optional_message').val();

  if(cat_id == null){
    alert("You must select a category");
    return;
  }
  else if (mess_id == null) {
    alert("You must select a pre defined message");
    return;
  }
  else if (points == ""){
    alert("You must add in some points");
    return;
  }

  var data = {
    "cat_id": cat_id,
    "mess_id": mess_id,
    "student": student_id,
    "points": points,
    "optional_message": optional_message,
    "subject_slug":course
  }

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
      url: "/feedback/",
      data: JSON.stringify(data),
      type: 'POST',
      contentType: 'application/json',
      dataType: "json",
      success: function() {
      },

  });
  var host = location.protocol + "//" + window.location.host;
  window.location.replace("/student/my-provided-feedback/")

});

function updateHtml(colour,message_set,cat_name,cat_id) {
  // Updates the cards shown in the message card. This allows the messages shown to change dependent
  // on which category is selected
  var cat_messages = "";
  for (var retrieved_message in message_set){
    for (var message_id in all_messages){
      if (message_set[retrieved_message] == message_id){
        cat_messages += `<div class="card message-card fb-border mess-item" id="` + message_id + `" style="border-color:` + colour + `">`
                        + `<div class="card-body text-center">`
                        + `<b class="message-heading">` + all_messages[message_id] + `</b>`
                        + `</div></div><br />`
      }
    }
  }
  $('.messages').html(cat_messages);
}

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
