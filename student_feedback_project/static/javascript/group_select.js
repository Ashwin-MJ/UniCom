var addclass = 'color';
$('.students').click(function(e) {
  $(this).toggleClass(addclass);
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

$('#individual-feedback-form').submit(function(){
  var res=[];
  $('.students').each(function(){
    if($(this).hasClass('color')){
      res.push($(this).attr('id'))
    }
  })
  var course_slug = document.getElementsByClassName("container")[1].id;

  var jsonText = JSON.stringify(res);
  console.log(jsonText);
  var cookieText = "students=" + jsonText + ';'
  document.cookie = cookieText;
  var act = "/lecturer/" + course_slug + "/" + res[0] + "/add-individual-feedback/";
  console.log(act)
  document.getElementById("individual-feedback-form").setAttribute("action",act);
  return true;
});
