$('#invites-form').submit(function(){
  var students=[];
  $('.students').each(function(){
    if($(this).hasClass('color')){
      students.push($(this).attr('id'))
    }
  })

  emails = []
  $('.emails').each(function(){
    if(this.value != ""){
      emails.push(this.value);
    }
  })

  if(students.length == 0 && emails.length == 0){
    alert("You must either select students or type in an email address");
    return false;
  }

  if(students.length != 0){
    var jsonText = JSON.stringify(students);
    var cookieText = "students=" + jsonText + ';max-age=1'
    document.cookie = cookieText;
  }

  var jsonText = JSON.stringify(emails);
  var cookieText = "emails=" + jsonText + ';max-age=1'
  document.cookie = cookieText;


  return true;

});

function addEmail() {
  var text = document.createElement('div');
  text.setAttribute("class", "card custom-card");
  text.innerHTML = '<input type="text" class="emails" placeholder="example@university.com" style="width:100%;">'
  document.getElementById("emails").appendChild(text);
}
