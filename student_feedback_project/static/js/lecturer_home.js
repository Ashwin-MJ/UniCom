"use strict";

function getCats(lect_id, param){
	var Url = "http://127.0.0.1:8000/FeedbackSortedByPoints"
	var httpRequest = new XMLHttpRequest();
	httpRequest.onreadystatechange = function(){
		if (this.readyState == 4 && this.status == 200) {			
			var sortedFb = JSON.parse(this.responseText);
		}
	}
	httpRequest.open("GET", Url, true);
	httpRequest.send();
}

function getCatsa(lect_id, param){
	const Url = "http://127.0.0.1:8000/Feedback_with_categoryList/";	
	var httpRequest = new XMLHttpRequest();
	httpRequest.onreadystatechange = function(){
		if (this.readyState == 4 && this.status == 200) {
			var categories = JSON.parse(this.responseText);			
			fetchStud(lect_id, categories, param);
		}
	};	
	httpRequest.open("GET", Url, true);
	httpRequest.send();	
}

function fetchStud(lect_id, param){
	const Url = "http://127.0.0.1:8000/Feedback_with_studentList/";	
	var httpRequest = new XMLHttpRequest();
	httpRequest.onreadystatechange = function(){
		if (this.readyState == 4 && this.status == 200) {
			var students = JSON.parse(this.responseText);	
			sort(lect_id, students, param);

		}
	};	
	httpRequest.open("GET", Url, true);
	httpRequest.send();	
}

function sort(lect_id, students, param){	
	switch(param){
		case "points":
			var Url = "http://127.0.0.1:8000/FeedbackSortedByPoints";
			break;
		case "date":
			var Url = "http://127.0.0.1:8000/FeedbackSortedByDate";
			break;
		case "course":
			var Url = "http://127.0.0.1:8000/FeedbackSortedByCourse";
			break;
		default:
		break
	}		
	var httpRequest = new XMLHttpRequest();
	httpRequest.onreadystatechange = function(){
		if (this.readyState == 4 && this.status == 200) {			
			var sortedFb = JSON.parse(this.responseText);
			
			//make lecturer id the one in the database then remove fb that is not from this lecturer
			var lecturer_id = lect_id + 5;			
			for(var i=0; i<sortedFb.length; i++){
				if(sortedFb[i].lecturer != lecturer_id){
					sortedFb.splice(i,1);
				}
			}
			
			//for every feedback replace the id number given by JSON for student to the name
			for(var fb of sortedFb){
				var fb_id = fb["student_id"];				
				
				for(var stud of students){
					if(stud["feedback_id"] == fb_id){
						fb["student_id"] = stud["studentName"];
					}
				}				
			}			
			
			
			//place this parsed data into the page
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
          + "<b>" + fb["category_id"] + "</b>"
          + "<p>"
          + fb["message"] + "<br />"
		  + fb["student_id"] + "<br />"
          + fb["points"]
          + "</p>"
          + "</div>";
		}
	document.getElementById("fb-list").innerHTML = mytext;
}



/* DATA SENT THROUGH FROM SERVER
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