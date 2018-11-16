function Validate() {
	var almeno_uno;
	var value = document.getElementsByName('username')[0].value;
	if (!/^\s*$/.test(value)) {
		return true;
	}
	value = document.getElementsByName('email')[0].value;
	if (!/^\s*$/.test(value)) {
		return true;
	}
	value = document.getElementsByName('first_name')[0].value;
	if (!/^\s*$/.test(value)) {
		return true;
	}
	value = document.getElementsByName('last_name')[0].value;
	if (!/^\s*$/.test(value)) {
		return true;
	}
	value = document.getElementsByName('data_inizio_year')[0].value;
	if (value != "") {
		return true;
	}
	value = document.getElementsByName('data_fine_year')[0].value;
	if (value != "") {
		return true;
	}

	alert("Devi inserire almeno un campo");
	return false; 
}