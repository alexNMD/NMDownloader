$(document).ready(function(){
	if (localStorage.UI_type == 'large') {
	  $("#change_interface").prop("checked", false);
	} else if (localStorage.UI_type == 'small') {
	  $("#change_interface").prop("checked", true);
	} else {
	  $("#change_interface").prop("checked", false);
	}
});

  $("#change_interface").change(function() {
	if ($('#change_interface').prop('checked')) {
	  $("#UI_large").hide();
	  $("#UI_small").show();
	  localStorage.setItem("UI_type","small")
	} else {
	  $("#UI_large").show();
	  $("#UI_small").hide();
	  localStorage.setItem("UI_type","large")
	}
});

$(document).ready(function() {
	if ($('#change_interface').prop('checked')) {
	  $("#UI_large").hide();
	  $("#UI_small").show();
	  localStorage.setItem("UI_type","small")
	} else {
	  $("#UI_large").show();
	  $("#UI_small").hide();
	  localStorage.setItem("UI_type","large")
	}
});

// Get the button:
mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
};

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
};