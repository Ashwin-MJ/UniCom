var addclass = 'color';
$('.students').click(function(e) {
  $(this).toggleClass(addclass);
});

$('#add-group-feedback').click(function(){
  var res=[];
  $('.students').each(function(){
    if($(this).hasClass('color')){
      res.push($(this).attr('id'))
    }
  })
  if(res.length < 2){
    alert("Please select at least 2 students to provide group feedback.")
  }
  else{
    var jsonText = JSON.stringify(res);
    var cookieText = "students=" + jsonText + ';'
    document.cookie = cookieText;
  }

})
