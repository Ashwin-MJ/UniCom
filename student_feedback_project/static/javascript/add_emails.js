$('#invites-form').submit(function(){
  var res=[];
  $('.students').each(function(){
    if($(this).hasClass('color')){
      res.push($(this).attr('id'))
    }
  })
  
  if(res.length != 0){
    var jsonText = JSON.stringify(res);
    var cookieText = "students=" + jsonText + ';'
    document.cookie = cookieText;
  }
  
  res = []
  $('.emails').each(function(){
  //if($(this).attr('value') != "example@university.com"){
  res.push(this.value);
  //}
  })
  var jsonText = JSON.stringify(res);
  var cookieText = "emails=" + jsonText + ';'
  document.cookie = cookieText;
  
  return true;
  /*
  var xhr = new XMLHttpRequest();
  xhr.open("POST", window.location.href , true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(
    JSON.stringify({
      value: value
    })
  );
  */

});

function addEmail() {
  var text = document.createElement('div');
  text.setAttribute("class", "card custom-card");
  text.innerHTML = '<input type="text" class="emails" value="example@university.com" style="width:100%;">'
  document.getElementById("emails").appendChild(text);
}

