"use strict";

function fetchStud(fb_keep, sort_param, keep_param){
	var host = location.protocol + "//" + window.location.host;
	const Url = host + "/Feedback_with_studentList/";
	var httpRequest = new XMLHttpRequest();
	httpRequest.onreadystatechange = function(){
		if (this.readyState == 4 && this.status == 200) {
			var students = JSON.parse(this.responseText);
			fetchFromUser(fb_keep, students, sort_param, keep_param);

		}
	};
	httpRequest.open("GET", Url, true);
	httpRequest.send();
}

function fetchFromUser(fb_keep, students, sort_param, keep_param){
	var host = location.protocol + "//" + window.location.host;
	const Url = host + "/Feedback_with_from_userList/";
	var httpRequest = new XMLHttpRequest();
	httpRequest.onreadystatechange = function(){
		if (this.readyState == 4 && this.status == 200) {
			var fromUsers = JSON.parse(this.responseText);
			fetchCatColour(fb_keep, students, fromUsers, sort_param, keep_param);

		}
	};
	httpRequest.open("GET", Url, true);
	httpRequest.send();
}

function fetchCatColour(fb_keep, students, fromUsers, sort_param, keep_param){
	var host = location.protocol + "//" + window.location.host;
	const Url = host + "/Feedback_with_categoryList/";
	var httpRequest = new XMLHttpRequest();
	httpRequest.onreadystatechange = function(){
		if (this.readyState == 4 && this.status == 200) {
			var catColours = JSON.parse(this.responseText);
			sort(fb_keep, students, fromUsers, catColours, sort_param, keep_param);

		}
	};
	httpRequest.open("GET", Url, true);
	httpRequest.send();
}

function sort(fb_keep, students, fromUsers, catColours, sort_param, keep_param){
	var host = location.protocol + "//" + window.location.host;
	switch(sort_param){
		case "points":
			var Url = host + "/FeedbackSortedByPoints";
			break;
		case "date":
			var Url = host + "/FeedbackSortedByDate";
			break;
		case "course":
			var Url = host + "/FeedbackSortedByCourse";
			break;
		default:
	}
	var httpRequest = new XMLHttpRequest();
	httpRequest.onreadystatechange = function(){
		if (this.readyState == 4 && this.status == 200) {
			var sortedFb = JSON.parse(this.responseText);

			//for every feedback replace the id number given by JSON for student and from user to the name and see if feedback is recent (5mins)
			for(var fb of sortedFb){
				var stud_id = fb["student"];
				for(var stud of students){
					if(stud["student_id"] == stud_id){
						fb["student"] = stud["studentName"];
					}
				}

				var from_user_id = fb["from_user"];

				for(var user of fromUsers){
					if(user.from_user_id == from_user_id){
						fb.from_user = user.fromUserName;
					}
				}

				var fb_date= new Date(fb['datetime_given']);
				var now_date = new Date();
				var five_mins = new Date(5*60000);
				if((now_date - fb_date) < five_mins){
					fb.is_recent = true;
				}
				else{
					fb.is_recent = false;
				}

				var fb_cat = fb.category;
				for(var cat of catColours){
					if(cat.category_id == fb_cat){
						fb.catColour = cat.categoryColour;
					}
				}

			}

			switch(keep_param){
				case "from_user":
					//remove fb that is not from the parameter we want to keep
					var from_user_name = fb_keep;
					for(var i=0; i<sortedFb.length; i++){
						if(sortedFb[i].from_user != from_user_name){
							sortedFb.splice(i,1);
							i=-1;
						}
					}
					var footerType = "student";
					break;
				case "course":
					var course_name = fb_keep;
					for(var i=0; i<sortedFb.length; i++){
						if(sortedFb[i].courseName != course_name){
							sortedFb.splice(i,1);
							i=-1;
						}
					}
					var footerType = "student";
					break;
				case "course-student":
					var course_name = fb_keep.split(",")[0];
					for(var i=0; i<sortedFb.length; i++){
						if(sortedFb[i].courseName != course_name){
							sortedFb.splice(i,1);
							i=-1;
						}
					}
					var student_name = fb_keep.split(",")[1];
					for(var i=0; i<sortedFb.length; i++){
						if(sortedFb[i].student != student_name){
							sortedFb.splice(i,1);
							i=-1;
						}
					}
					var footerType = "from_user";
					break;
				case "student":
					var student_name = fb_keep;
					for(var i=0; i<sortedFb.length; i++){
						if(sortedFb[i].student != student_name){
							sortedFb.splice(i,1);
							i=-1;
						}
					}
					var footerType = "from_user";
					break;
				default:
			}

			//place this parsed data into the page
			show(sortedFb, footerType);
		}
	};
	httpRequest.open("GET", Url, true);
	httpRequest.send();
}


function show(sorted_fb, footerType){
	var fb_text = '';
	for (var fb of sorted_fb){
		var myDate = new Date(fb.datetime_given);
		 var month=new Array();
		  month[0]="Jan";
		  month[1]="Feb";
		  month[2]="Mar";
		  month[3]="Apr";
		  month[4]="May";
		  month[5]="Jun";
		  month[6]="Jul";
		  month[7]="Aug";
		  month[8]="Sep";
		  month[9]="Oct";
		  month[10]="Nov";
		  month[11]="Dec";
		  var hours = myDate.getHours();
		  var minutes = myDate.getMinutes();
		  var ampm = hours >= 12 ? 'p.m.' : 'a.m.';
		  hours = hours % 12;
		  hours = hours ? hours : 12;
		  minutes = minutes < 10 ? '0'+minutes : minutes;
		  var strTime = hours + ':' + minutes + ' '+ ampm;
		var showDate = ' ' + month[myDate.getMonth()] + '. ' + myDate.getDate() + ', ' + myDate.getFullYear() + ', ' + strTime;
		if(footerType == "student")
			var footer = 'Given to ' + fb.student;
		else
			var footer = fb.from_user;
		if(fb.is_recent){
			fb_text += '<div class="card recent custom-card text-white fb-border" style="border-color:' + fb.catColour + '">';
		}
		else
			fb_text += '<div class="card custom-card fb-border" style="border-color:' + fb.catColour + '">';
		fb_text += '<b class="card-sub-heading" style="color:' + fb.catColour + '">' + fb.category + `</b>
          <div class="row" style="padding-bottom:1%">
            <div class="column left">
              <div class="border">
                <blockquote class="quote">`
                +  fb.pre_defined_message_id +'<br />';
                  if (fb.optional_message){
                  fb_text += '<em>"' + fb.optional_message + '"</em>'
				  }
                  fb_text += '<footer>' + footer + '</footer>'
                + `</blockquote>
              </div>
              Course: <em>` + fb.courseName + `</em><br />
              <i class="material-icons" style="font-size:70%;">calendar_today</i>` + showDate
            + `</div>
            <div class="column right-number">`
						+ '<div style="text-align:center; color:' + fb.catColour + '">'
            + fb.points + `<br />`
						+ `<h6>POINTS</h6>`
						+ `</div>`
            + `</div>
            </div>
          </div>`;
	}
	document.getElementById("fb-list").innerHTML = fb_text;
}




/* DATA SENT THROUGH FROM SERVER
[

category_id: "Cooperation"
date_given: "2019-01-09T12:53:24.045360Z"
datetime_given: "2019-01-09T12:53:24.045360Z"
feedback_id: 2
is_recent: false
lecturer_id: 7
optional_message: "I noticed how you helped Link complete his work."
points: 3
pre_defined_message: "Excellent team work today!"
student_id: "Harry Potter"
which_course_id: "MAT1Q"
__proto__: Object

category_id: "Participation"
date_given: "2019-01-09T12:53:24.462372Z"
datetime_given: "2019-01-09T12:53:24.462372Z"
feedback_id: 3
is_recent: false
lecturer_id: 7
optional_message: "If you require further clarification, feel free to drop by my office."
points: 5
pre_defined_message: "Very good question today. I'm sure you helped a lot of students by asking it!"
student_id: 5
which_course_id: "ARH01"
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
