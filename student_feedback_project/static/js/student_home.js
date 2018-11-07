	function sortByPoints(){
		var list, i, switching, b, shouldSwitch;
	  list = document.getElementsByClassName("card");
	  switching = true;
	  while (switching) {
	    switching = false;
	    b = list.getElementById("points");
	    for (i = 0; i < (b.length - 1); i++) {
	      //start by saying there should be no switching:
	      shouldSwitch = false;
	      /*check if the next item should
	      switch place with the current item:*/

	      if (Number(b[i].innerHTML) > Number(b[i + 1].innerHTML)) {
	        /*if next item is numerically
	        lower than current item, mark as a switch
	        and break the loop:*/
	        shouldSwitch = true;
	        break;
	      }
	    }
	    if (shouldSwitch) {
	      /*If a switch has been marked, make the switch
	      and mark the switch as done:*/
	      b[i].parentNode.insertBefore(b[i + 1], b[i]);
	      switching = true;
	    }
	  }
	}	
