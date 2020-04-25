window.addEventListener('load', () => {

	var forms = document.querySelectorAll('.needs-validation');
	var inputs = document.querySelectorAll('input');

	forms.forEach(element => {
		element.addEventListener('submit', (event) => {
			if (element.checkValidity() === false) {
				event.preventDefault();
				event.stopPropagation();
				element.classList.add('was-validated');
			}
		});


	});

	inputs.forEach(element => {
		element.addEventListener('input', (event) => {
			var item = document.querySelector('.bottom-help-message');
			item.innerHTML = "";
		});
	});
});