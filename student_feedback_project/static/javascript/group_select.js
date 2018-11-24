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
  if( !window.localStorage) alert("Sorry, you're using an ancient browser");
  else {
    localStorage.myArray = JSON.stringify(res);
  }
})
