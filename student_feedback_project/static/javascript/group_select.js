var addclass = 'color';
$('.students').click(function(e) {
  $(this).toggleClass(addclass);
});

$('#select-all').click(function(e) {
  $('.students').each(function(e) {
    $(this).toggleClass(addclass);
  });
});

$('#group-feedback-form').submit(function(){
  var res=[];
  $('.students').each(function(){
    if($(this).hasClass('color')){
      res.push($(this).attr('id'))
    }
  })

  if(res.length < 2){
    alert("Please select at least 2 students to provide group feedback.");
    return false;
  }
  else{
    var jsonText = JSON.stringify(res);
    var cookieText = "students=" + jsonText + ';'
    document.cookie = cookieText;
    return true;
  }
});

$('#invites-form').submit(function(){
  var res=[];
  $('.students').each(function(){
    if($(this).hasClass('color')){
      res.push($(this).attr('id'))
    }
  })

  if(res.length == 0){
    alert("Please select at least 1 students to send the course token to.");
    return false;
  }
  else{
    var jsonText = JSON.stringify(res);
    var cookieText = "students=" + jsonText + ';'
    document.cookie = cookieText;
    return true;
  }
});

$('#individual-feedback-form').submit(function(){
  var res=[];
  $('.students').each(function(){
    if($(this).hasClass('color')){
      res.push($(this).attr('id'))
    }
  })

  if(res.length < 1){
    alert("Please select at least 1 student to provide individual feedback.");
    return false;
  }

  var course_slug = document.getElementsByClassName("container")[1].id;

  var jsonText = JSON.stringify(res);

  var cookieText = "indiv_students=" + jsonText + ';path=/lecturer/'+course_slug + "/";
  document.cookie = cookieText;
  var act = "/lecturer/" + course_slug + "/" + res[0] + "/add-individual-feedback/";

  document.getElementById("individual-feedback-form").setAttribute("action",act);
  return true;
});
