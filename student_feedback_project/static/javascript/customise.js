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
    console.log(csrftoken);
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
