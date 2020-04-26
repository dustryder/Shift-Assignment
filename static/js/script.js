window.addEventListener('load', () => {

	var forms = document.querySelectorAll('.needs-validation');
	var inputs = document.querySelectorAll('input');
	var lookup_datalist = document.querySelector('#student_name');
	var lookup_input = document.querySelector('#student_name_lookup');
	var lookup_data_id;

	forms.forEach(element => {
		element.addEventListener('submit', (event) => {
			if (element.checkValidity() === false) {
				event.preventDefault();
				event.stopPropagation();
				element.classList.add('was-validated');
			} else if (lookup_data_id) {
				let hiddenStudentIdInput = document.querySelector('#hidden_studentid');
				hiddenStudentIdInput.value = lookup_data_id;

			}
		});

		element.addEventListener('reset', (event) => {
			var item = document.querySelectorAll('.bottom-ephemeral-message');
			item.forEach(message => {
				element.classList.remove('was-validated');
				message.innerHTML = "";
			});

		});
	});

	inputs.forEach(element => {
		element.addEventListener('input', (event) => {
			var item = document.querySelectorAll('.bottom-ephemeral-message');
			item.forEach(message => {
				message.innerHTML = "";
			});

			if (element.id === "student_name_lookup") {

				let choice = document.querySelector(`option[value="${element.value}"]`);
				if (choice) {
					lookup_data_id = choice.getAttribute("data-id");
				} else {
					lookup_data_id = 0;
				}
			}
		});
	});

});

