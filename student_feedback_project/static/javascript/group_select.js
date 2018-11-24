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
  var jsonText = JSON.stringify(res);
  document.cookie = jsonText;
})
