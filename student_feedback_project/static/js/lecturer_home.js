"use strict";

function sort(lect_id){
	const Url = "http://127.0.0.1:8000/Feedback_with_categoryList/";	
	var httpRequest = new XMLHttpRequest();
	httpRequest.onreadystatechange = function(){
		if (this.readyState == 4 && this.status == 200) {
			var categories = JSON.parse(this.responseText);			
			fetchStud(lect_id, categories);
		}
	};	
	httpRequest.open("GET", Url, true);
	httpRequest.send();	
}

function fetchStud(lect_id, categories){
	const Url = "http://127.0.0.1:8000/Feedback_with_studentList/";	
	var httpRequest = new XMLHttpRequest();
	httpRequest.onreadystatechange = function(){
		if (this.readyState == 4 && this.status == 200) {
			var students = JSON.parse(this.responseText);			
			pointsSort(lect_id, categories, students);
		}
	};	
	httpRequest.open("GET", Url, true);
	httpRequest.send();	
}

function pointsSort(lect_id, categories, students){	
	const Url = "http://127.0.0.1:8000/FeedbackSortedByPoints";	
	var httpRequest = new XMLHttpRequest();
	httpRequest.onreadystatechange = function(){
		if (this.readyState == 4 && this.status == 200) {			
			var sortedFb = JSON.parse(this.responseText);
			
			var lecturer_id = lect_id + 5;			
			for(var i=0; i<sortedFb.length; i++){
				if(sortedFb[i].lecturer != lecturer_id){
					sortedFb.splice(i,1);
				}
			}				
			for(var fb of sortedFb){
				var fb_id = fb["category"];
				
				for(var cat of categories){
					if(cat["feedback_id"] == fb_id){
						fb["category"] = cat["categoryName"];
					}
				}
				
				for(var stud of students){
					if(stud["feedback_id"] == fb_id){
						fb["student"] = stud["studentName"];
					}
				}				
			}			
			
			show(sortedFb);
		}
	};
	
	httpRequest.open("GET", Url, true);
	httpRequest.send();
}


function show(sortedFb){
	var mytext = '<p class="card-text"></p>';	
        for (var fb of sortedFb){
        mytext = mytext + '<div class="card" style="padding-left:10px; margin-top:10px">'
          + "<b>" + fb["category"] + "</b>"
          + "<p>"
          + fb["message"] + "<br />"
		  + fb["student"] + "<br />"
          + fb["points"]
          + "</p>"
          + "</div>";
		}
	document.getElementById("fb-list").innerHTML = mytext;
}



/* DATA SENT THROUGH FROM FEEDBACKLIST
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
"which_class":"MAT1Q",
"category":1
},
*/