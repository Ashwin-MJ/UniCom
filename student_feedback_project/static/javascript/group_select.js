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
