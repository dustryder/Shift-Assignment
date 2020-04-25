window.addEventListener('load', () => {
	var forms = document.querySelectorAll('.needs-validation');
	forms.forEach(element => {
		element.addEventListener('submit', (event) => {
			if (element.checkValidity() === false) {
				event.preventDefault();
				event.stopPropagation();
				element.classList.add('was-validated');
			}
		});
	});
});