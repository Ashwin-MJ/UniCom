	function sort_by_points(){
		httpGetAsync("http://127.0.0.1:8000/GET/", null);
		
	}	

	
	function httpGetAsync(theUrl, callback)
{
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() { 
        if (httpRequest.readyState == 4 && httpRequest.status == 200)
			var data = httpRequest.responseText;
			if(callback){
				callback(data);
			}
    }
    httpRequest.open("GET", theUrl, true); // true for asynchronous 
    httpRequest.send(null);
}