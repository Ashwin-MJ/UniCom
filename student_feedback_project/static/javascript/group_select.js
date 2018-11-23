var addclass = 'color';
$('.students').click(function(e) {
  $(this).toggleClass(addclass);
});

$(':submit').click(function(){
  var res=[];
  $('.students').each(function(){
    if($(this).hasClass('color')){
      res.push($(this).attr('id'))
    }
  })
  alert(res)
})
