window.addEventListener('load', () => {

	var forms = document.querySelectorAll('.needs-validation');
	var inputs = document.querySelectorAll('input');
	//Default variables that will fail serverside validation if an option is not selected or valid unique identifier is not given
	var lookupDataStudentId = "Invalid";
	var lookupDataCourseCode = "Invalid";

	//jQuery witchcraft for popper.js
	$(function () {
	  $('[data-toggle="tooltip"]').tooltip()
	})


	//Client side validation with custom bootstrap validators
	forms.forEach(element => {
		element.addEventListener('submit', () => {
			if (element.checkValidity() === false) {
				event.preventDefault();
				event.stopPropagation();
				element.classList.add('was-validated');
			}
		});
	});


	//Insert relevant data to hidden input fields for backend
	forms.forEach(element => {
		element.addEventListener('submit', () => {
			if (lookupDataStudentId) {
				let hiddenStudentIdInput = document.querySelector('#hidden-studentid');
				hiddenStudentIdInput.value = lookupDataStudentId;
			}

			if (lookupDataCourseCode) {
				var hiddenCourseCodeInput = document.querySelector('#hidden-coursecode');
				if (hiddenCourseCodeInput) {
					hiddenCourseCodeInput.value = lookupDataCourseCode;
				}
			}
		});
	});


	//Clear bottom messages and bootstrap custom validators on reset
	forms.forEach(element => {
		element.addEventListener('reset', (event) => {
			var item = document.querySelectorAll('.bottom-ephemeral-message');
			element.classList.remove('was-validated');
			item.forEach(message => {
				message.innerHTML = "";
			});
		});
	});


	//Clears bottom messages on changing values in input fields
	inputs.forEach(element => {
		element.addEventListener('input', () => {
			var item = document.querySelectorAll('.bottom-ephemeral-message');
			if (element.id !== "course-title-lookup") {
				item.forEach(message => {
					message.innerHTML = "";
				});
			}
		});
	});


	//Retrieves custom data contained within selected datalist option
	inputs.forEach(element => {
		element.addEventListener('input', () => {
			let choice = document.querySelector(`option[value="${element.value}"]`);
			if (choice) {
				//Set value to data contained in data-id propery of option elements
				item = choice.getAttribute("data-id");
				if (element.id === "student-name-lookup") lookupDataStudentId = item;
				if (element.id === "course-title-lookup") lookupDataCourseCode = item;

			} else {
				//If an option is not selected, set the value to typed value
				item = element.value;
				if (element.id === "student-name-lookup") lookupDataStudentId = item;
				if (element.id === "course-title-lookup") lookupDataCourseCode = item;
			}

		});
	});

});

