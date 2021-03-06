"use strict";

function sort_smart(sort_param, footerType, insert_into_id, ...args){
	//get sorted fb according to sort_param
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
			var allSortedFb = JSON.parse(this.responseText);
			var sortedFb = [];
			//for every feedback see if feedback is recent (5mins) and if it's in the list we want
			for(var fb of allSortedFb){
				if(args.includes(fb.feedback_id)){
					sortedFb.push(fb)
					var fb_date= new Date(fb['datetime_given']);
					var now_date = new Date();
					var five_mins = new Date(5*60000);
					if((now_date - fb_date) < five_mins){
						fb.is_recent = true;
					}
					else{
						fb.is_recent = false;
					}
				}
			}
			show(sortedFb, footerType, insert_into_id);
		}
	};
	httpRequest.open("GET", Url, true);
	httpRequest.send();
}

function sort(fb_keep, sort_param, keep_param, recent, catDict){
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

			//for every feedback see if feedback is recent (5mins)
			var shouldReduce = false;
			for(var i=0; i<sortedFb.length; i++){
				var fb_date= new Date(sortedFb[i].datetime_given);
				var now_date = new Date();
				//if in recent feedback card (given by param) then delete all feedback older than a week
				if(recent != undefined){
					var one_week = new Date(7*24*60*60*1000)
					 if((now_date - fb_date) > one_week){
						 sortedFb.splice(i,1);
						 shouldReduce = true;
					 }
				}
				if(i == sortedFb.length){
					i-=1;
					shouldReduce = false;
				}
				var five_mins = new Date(5*60000);
				if((now_date - fb_date) < five_mins){
					sortedFb[i].is_recent = true;
				}
				else{
					sortedFb[i].is_recent = false;
				}
				if(catDict != null && catDict[sortedFb[i].categoryName] != null)
					sortedFb[i].categoryColour = catDict[sortedFb[i].categoryName];
				if(shouldReduce){
					i-=1;
					shouldReduce = false;
				}
			}


			switch(keep_param){
				case "from_user":
					//remove fb that is not from the parameter we want to keep
					var from_user_name = fb_keep;
					for(var i=0; i<sortedFb.length; i++){
						if(sortedFb[i].fromUserName != from_user_name){
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
					var course_name = fb_keep.split("$")[0];
					for(var i=0; i<sortedFb.length; i++){
						if(sortedFb[i].courseName != course_name){
							sortedFb.splice(i,1);
							i=-1;
						}
					}
					var student_name = fb_keep.split("$")[1];
					for(var i=0; i<sortedFb.length; i++){
						if(sortedFb[i].studentName != student_name){
							sortedFb.splice(i,1);
							i=-1;
						}
					}
					var footerType = "from_user";
					break;
				case "student":
					var student_name = fb_keep;
					for(var i=0; i<sortedFb.length; i++){
						if(sortedFb[i].studentName != student_name){
							sortedFb.splice(i,1);
							i=-1;
						}
					}
					var footerType = "from_user";
					break;
				default:
			}

			//place this parsed data into the page
			show(sortedFb, footerType, 'fb-list');
		}
	};
	httpRequest.open("GET", Url, true);
	httpRequest.send();
}


function show(sorted_fb, footerType, insert_into_id){
	var fb_text = '';
	if (sorted_fb.length == 0) {
		fb_text += `<div class="card custom-card fb-border">
			<b class="card-sub-heading">
				No Feedback Yet
			</b>
			<div class="card custom-border">
				<blockquote class="quote">`;
				if(footerType == 'from_user'){
					fb_text += 'You have not received any feedback yet<br />';
				}
				else {
					fb_text += 'You have not given any feedback yet<br />';
				}
				fb_text += `</blockquote>
			</div>
		</div>`;
	}
	for (var fb of sorted_fb){
		var myDate = new Date(fb.datetime_given);
		 var month=new Array();
		  month[0]="Jan";
		  month[1]="Feb";
		  month[2]="March";
		  month[3]="April";
		  month[4]="May";
		  month[5]="June";
		  month[6]="July";
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
			if(strTime == '12:00 a.m.') strTime = 'midnight';
		var showDate = ' ' + month[myDate.getMonth()] + ' ' + myDate.getDate() + ', ' + myDate.getFullYear() + ', ' + strTime;
		if(footerType == "student")
			var footer = 'Given to ' + fb.studentName;
		else{
			var footer = 'From ' + fb.fromUserName;
			if(fb.studentColour != null)
				fb.categoryColour = fb.studentColour;
		}
		if(fb.is_recent){
			fb_text += '<div class="card recent custom-card text-white fb-border" style="border-color:' + fb.categoryColour + '">';
		}
		else{
			fb_text += '<div class="card custom-card fb-border" style="border-color:' + fb.categoryColour + '">';
		}
		if( window.location.href.includes('my-provided-feedback'))
			fb_text += '<i class="material-icons delete-icon" id="' + fb.feedback_id + '">delete</i>';
		if(window.location.href.includes('lecturer/courses/'))
			fb_text += '<i class="material-icons delete-icon delete-icon-course" id="' + fb.feedback_id + '">delete</i>';

		fb_text += '<b class="card-sub-heading" style="color:' + fb.categoryColour + '">';
		fb_text += '<img class="icon" src="/media/' + fb.image + '"/>'
						+ ' ' + fb.categoryName + `</b>
          <div class="row" style="padding-bottom:1%">
            <div class="column left">
              <div class="card custom-border">
                <blockquote class="quote">`
                +  fb.preDefMessageText +'<br />';
                  if (fb.optional_message){
                  fb_text += '<em>"' + fb.optional_message + '"</em>'
				  				}
                  fb_text += '<footer>' + footer + '</footer>'
                + `</blockquote>
              </div>`;
							if( window.location.href.includes('lecturer/courses/'))
								fb_text += `From: <em>` + fb.fromUserName + `</em><br />`
							else
              	fb_text += `Course: <em>` + fb.courseName + `</em><br />`;
              fb_text += `<i class="material-icons" style="font-size:70%;">calendar_today</i>` + showDate
            + `</div>
            <div class="column right-number">`
						+ '<div style="text-align:center; color:' + fb.categoryColour + '">'
            + fb.points + `<br />`
						+ `<h6>POINTS</h6>`
						+ `</div>`
            + `</div>
            </div>
          </div>`;
	}
	document.getElementById(insert_into_id).innerHTML = fb_text;
}
