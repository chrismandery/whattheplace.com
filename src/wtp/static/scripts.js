function cleanInputDefault(inputId) {
	inputField = document.getElementById(inputId);
	if (inputField.value == inputField.defaultValue)
		inputField.value = "";
}

function imageIdBoxSubmit(e, content) {
	if (window.event)
		keyCode = window.event.keyCode;
	else
		keyCode = e.which;
	
	if (keyCode == 13) {
		imageId = parseInt(content)
		if (!isNaN(imageId))
			setUrl("/Show/" + imageId + "/");
		
		return false;
	}
	else
		return true;
}

function setUrl(url) {
	document.location = url;
}

function solutionBoxCheck() {
	imageId = document.getElementById("input-imageid").value;
	solution = document.getElementById("input-solution").value;
	
	if (!solution.length)
		return;
	
	param = "image=" + imageId + "&solution=" + solution;
	
	request = new XMLHttpRequest();
	request.open("POST", "/Guess/", true);
	
	request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	request.setRequestHeader("Content-length", param.length);
	request.setRequestHeader("Connection", "close");
	request.setRequestHeader('X-CSRFToken', document.getElementsByName("csrfmiddlewaretoken")[0].value);
	request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
	
	request.onreadystatechange = function() {
		if (request.readyState == 4) {
			document.getElementById("input-submit").removeAttribute("disabled");
			
			if (request.status == 200) {
				if (request.responseText == "right")
					document.location.reload();
				else
					document.getElementById("input-solution").setAttribute("class", "wronganswer");
			}
			else {
				alert("Server returned an error (HTTP " + request.status + ").");
			}
		}
	};
	
	document.getElementById("input-submit").setAttribute("disabled", "disabled");
	
	request.send(param);
}

function solutionBoxEdited(e) {
	document.getElementById("input-solution").removeAttribute("class");
	
	if (window.event)
		keyCode = window.event.keyCode;
	else
		keyCode = e.which;
	
	if (keyCode == 13) {
		solutionBoxCheck();
		return false;
	}
	else
		return true;
}
