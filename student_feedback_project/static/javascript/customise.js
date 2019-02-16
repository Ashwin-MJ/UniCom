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
  var cat_id = this.id;
  var cat_name = $(this).parent().find("b").html();

  $('.modal-edit-cat-header').html("Edit \"" + cat_name + "\"");

  cat_name = cat_name.replace("&amp;", "&")

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

    location.reload()

  });

});

$('.create-cat-icon').click(function(e) {

  document.getElementById("new_cat_colour").value = "#009999";

  $('.submit-add-cat-form').on('click', function(){

    var new_name = $('#id_new_name').val();
    var new_colour = $('#new_cat_colour').val()

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
        url: "/category/",
        data: JSON.stringify(data),
        type: 'POST',
        contentType: 'application/json',
        dataType: "json",
        success: function() {
        },
    });

    location.reload()

  });

});



$('.category').on('click', function(){
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
        displayMessages(result)
      },
  });

});

function updateHtml(colour,message_set,cat_name) {
  var cat_messages = "";

  for (var retrieved_message in message_set){
    for (var message_id in all_messages){
      if (message_set[retrieved_message] == message_id){
        cat_messages += `<div class="card custom-card fb-border" style="border-color:` + colour + `">`
                        + `<div class="card-body text-center">`
                        + `<b class="card-sub-heading">` + all_messages[message_id] + `</b>`
                        + `<i class="material-icons delete-mess-icon" id=` + message_id + `>delete</i>`
                        + `</div></div><br />`
      }
    }
  }
  $('.cat-title').html(cat_name);
  $('.messages').html(cat_messages);

}

$('#all-messages').on('click','.delete-mess-icon', function() {
  console.log("Here")
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
