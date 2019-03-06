"use strict";

function sort(fb_keep, sort_param, keep_param, recent){
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
			for(var i=0; i<sortedFb.length; i++){
				var fb_date= new Date(sortedFb[i].datetime_given);
				var now_date = new Date();
				//if in recent feedback card (given by param) then delete all feedback older than a week
				if(recent != undefined){
					var one_week = new Date(7*24*60*60*1000)
					 if((now_date - fb_date) > one_week){
						 sortedFb.splice(i,1);
						 i-=1;
					 }
				}
				var five_mins = new Date(5*60000);
				if((now_date - fb_date) < five_mins){
					sortedFb[i].is_recent = true;
				}
				else{
					sortedFb[i].is_recent = false;
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
					var course_name = fb_keep.split(",")[0];
					for(var i=0; i<sortedFb.length; i++){
						if(sortedFb[i].courseName != course_name){
							sortedFb.splice(i,1);
							i=-1;
						}
					}
					var student_name = fb_keep.split(",")[1];
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
			var footer = 'Given to ' + fb.studentName;
		else
			var footer = 'From ' + fb.fromUserName;
		if(fb.is_recent){
			fb_text += '<div class="card recent custom-card text-white fb-border" style="border-color:' + fb.categoryColour + '">';
		}
		else{
			fb_text += '<div class="card custom-card fb-border" style="border-color:' + fb.categoryColour + '">';
		}
		if( window.location.href.includes('my-provided-feedback'))
			fb_text += '<i class="material-icons delete-icon" id="' + fb.feedback_id + '">delete</i>';
		fb_text += '<b class="card-sub-heading" style="color:' + fb.categoryColour + '">'
						+ '<img class="icon" src="/media/' + fb.image + '"/> '
						+ fb.categoryName + `</b>
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
              </div>
              Course: <em>` + fb.courseName + `</em><br />
              <i class="material-icons" style="font-size:70%;">calendar_today</i>` + showDate
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
	document.getElementById("fb-list").innerHTML = fb_text;
}
