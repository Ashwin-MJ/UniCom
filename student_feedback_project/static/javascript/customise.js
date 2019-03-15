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


$('.delete-cat-icon').click(function(e) {
  // This allows a category to be deleted
  // An issue is that when deleted, all feedback associated with that category is also deleted
  // This cannot be avoided, but the option should still be there. So a warning comes up
  var result = confirm("If you delete this category then every feedback you have given with this category will be deleted. Do you want to continue?");
  if(result){
    var cat_id = this.id;
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
        type: 'DELETE',
        contentType: 'application/json',
        success: function(result) {
          location.reload();
        },
    });
  }
});

$('.edit-cat-icon').click(function(e) {
  // This allows a category to be edited (text and colour)
  var cat_id = this.id;
  var cat_name = $(this).parent().find("b").text().trim();
  $('.modal-edit-cat-header').html("Edit \"" + cat_name + "\"");
  cat_name = cat_name.replace("&amp;", "&"); // Had to include this due to JSON issue
  document.getElementById("id_name").value = cat_name;
  document.getElementById("edit_cat_colour").value = "#009999";

  $('.submit-edit-cat-form').on('click', function(){
    var new_name = $('#id_name').val();
    var new_colour = $('#edit_cat_colour').val()
    var data = {
             "name": new_name,
             "colour": new_colour
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
        url: "/category/"+cat_id+"/",
        data: JSON.stringify(data),
        type: 'PATCH',
        contentType: 'application/json',
        dataType: "json",
        success: function() {
        },
    });
    location.reload() // Not sure why, but I had to move this out of the 'success' as it occasionally did not work
  });
});

$('.create-cat-icon').click(function(e) {
  // Pre set colour field to the default
  // This is needed if the submit is clicked without choosing a colour
  document.getElementById("new_cat_colour").value = "#009999";
  $('.submit-add-cat-form').on('click', function(){
    var new_name = $('#id_new_name').val();
    var new_colour = $('#new_cat_colour').val();
    var icon = $('.icon-highlighted').attr('id');

    if(new_name == ""){
      alert("You must type in a name for this category");
      return;
    }
    else if (new_colour == "") {
      alert("You must choose a colour");
      return;
    }
    else if (icon == null){
      alert("You must choose an icon");
      return;
    }
    var data = {
             "name": new_name,
             "colour": new_colour,
             "icon": icon
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
        url: "/category/",
        data: JSON.stringify(data),
        type: 'POST',
        contentType: 'application/json',
        dataType: "json",
        success: function() {
        },
    });
    location.reload() // Same issue as mentioned above
  });

});



$('.category').on('click', function(){
  // Dynamically display messages based on category selected
  var cat_id = $(this).find("i").attr('id');
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
        displayMessages(result,cat_id)
      },
  });

});

function updateHtml(colour,icon,message_set,cat_name,cat_id) {
  // Updates the cards shown in the message card. This allows the messages shown to change dependent
  // on which category is selected
  var cat_messages = "";
  console.log(message_set);
  for (var retrieved_message in message_set){
    for (var message_id in all_messages){
      if (message_set[retrieved_message] == message_id){
        cat_messages += `<div class="card custom-card fb-border" style="border-color:` + colour + `">`
                        + `<div class="card-body text-center">`
                        + `<b class="card-sub-heading"><img class="icon" src="` + icons[icon] + `"/> ` +  all_messages[message_id][0] + `</b>`
                        + `<i class="material-icons delete-mess-icon" id=` + message_id + `>delete</i>`

        if (all_messages[message_id][1]){
          cat_messages += `<i class="material-icons edit-mess-icon" data-toggle="modal" data-target="#editMessageModal" id=` + message_id +`>edit</i>`
        }
        cat_messages += `</div></div><br />`
      }
    }
  }
  $('.cat-title').html(cat_name);
  $('.cat-title').attr("id",cat_id); // Need to access cat_id in another method so set the id for easy retrieval
  $('#add-mess-icon').html("add_circle_outline"); // Only show add_message button if a category is selected
  $('.messages').html(cat_messages);
}

$('#all-messages').on('click','.delete-mess-icon', function() {
  // Same issue as mentioned above. When a message is deleted, all feedback associated with that message
  // will also be deleted. Give a warning for this
  var result = confirm("If you delete this message then every feedback you have given with this message will be deleted. Do you want to continue?");
  if(result){
    var mess_id = this.id;
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
        url: "/message/"+mess_id+"/",
        data: {},
        type: 'DELETE',
        contentType: 'application/json',
        success: function(result) {
          location.reload();
        },
    });
  }
});

$('.create-mess-icon').on('click',function(e) {
  // Dynamically update modal for this option
  // Then send POST request from here
  var cat_name = $('.cat-title').html();
  var cat_id = $('.cat-title').attr('id');

  $('.modal-add-mess-header').html("Add a new message for \"" + cat_name + "\"");
  $('.submit-add-mess-form').on('click', function(){
    var text = $('#id_new_text').val();
    var data = {
             "text": text,
             "category": cat_id
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
        url: "/message/",
        data: JSON.stringify(data),
        type: 'POST',
        contentType: 'application/json',
        dataType: "json",
        success: function() {
        },
    });
    location.reload() // Same issue as mentioned above
  });

});

$('#all-messages').on('click','.edit-mess-icon', function() {
  // This allows a message to be edited (text)
  var mess_id = this.id;
  var mess_text = $(this).parent().find("b").text().trim();
  $('.modal-edit-mess-header').html("Edit \"" + mess_text + "\"");
  document.getElementById("id_text").value = mess_text;

  $('.submit-edit-mess-form').on('click', function(){
    var new_text = $('#id_text').val();
    var data = {
             "text": new_text,
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
        url: "/message/"+mess_id+"/",
        data: JSON.stringify(data),
        type: 'PATCH',
        contentType: 'application/json',
        dataType: "json",
        success: function() {
        },
    });
    location.reload() // Same issue as mentioned above
  });
});

$(".all-icons").click(function (e){
  var highlight = "icon-highlighted";
  $('.all-icons').each(function() {
    if($(this).hasClass(highlight)){
      $(this).toggleClass(highlight);
    }
  });
  $(this).toggleClass(highlight);
});
