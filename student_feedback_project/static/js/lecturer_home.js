function sort(lect_id){
	const Url = "http://127.0.0.1:8000/FeedbackList/";	
	var httpRequest = new XMLHttpRequest();
	httpRequest.onreadystatechange = function(){
		if (this.readyState == 4 && this.status == 200) {
			var data = JSON.parse(this.responseText);		
			var lecturer_id = lect_id + 5;
			var i;
			for(i=0; i<data.length; i++){
				if(data[i].lecturer != lecturer_id){
					delete data[i];
				}
			}
			alert(data);
		}
	};
	
	httpRequest.open("GET", Url, true);
	httpRequest.send();
}


[
{
"date_given":"2018-11-27T15:00:35.211142Z",
"feedback_id":2,
"message":"You were very active in today's lesson!",
"points":3,
"lecturer":7,
"student":2,
"which_class":"MAT1Q",
"category":2
},

{
"date_given":"2018-11-27T15:00:35.502473Z",
"feedback_id":3,
"message":"Great marks in todays quiz!",
"points":5,
"lecturer":7,
"student":5,
"which_class":"ARH01",
"category":3
}
]

{
"date_given":"2018-11-27T15:00:34.911572Z",
"feedback_id":1,
"message":"Good job answering the question today!",
"points":4,
"lecturer":6,
"student":1,
"which_class":"MAT1Q","category":1
},