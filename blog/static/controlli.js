//form ricerca avanzata autore
function ValidateAutore() {
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
//form ricerca avanzata articolo
function ValidateArticolo() {
	var value = document.getElementsByName('parole')[1].value;
	if (!/^\s*$/.test(value)) {
		return true;
	}
	value = document.getElementsByName('id_autore')[0].value;
	if (value != "") {
		return true;
	}
	var sel = document.getElementsByName('keywords')[0];
	for (var i=0, len=sel.options.length; i<len; i++) {
        opt = sel.options[i];
        if ( opt.selected ) {
			return true;
		}		
	}
	value = document.getElementsByName('categoria')[0].value;
	if (value != "") {
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
	value = document.getElementsByName('citato')[0].value;
	if (!/^\s*$/.test(value)) {
		return true;
	}

	alert("Devi inserire almeno un campo");
	return false; 
}
//form menu 
function ValidateBase() {
	var value = document.getElementsByName('parole')[0].value;
	if (!/^\s*$/.test(value)) {
		return true;
	}

	alert("Prima devi inserire delle parole da cercare");
	return false; 
}
//form risultati ricerca sull'autore: nome, cognome
function ValidateRisultatiAutore() {
	var value = document.getElementsByName('first_name')[0].value;
	if (!/^\s*$/.test(value)) {
		return true;
	}
	value = document.getElementsByName('last_name')[0].value;
	if (!/^\s*$/.test(value)) {
		return true;
	}

	alert("Devi inserire almeno il nome o il cognome dell'autore che vuoi cercare");
	return false; 
}
//form risultati ricerca sull'articolo: parole (testo + titolo (solo ordinamento))
function ValidateRisultatiArticolo() {
	var value = document.getElementsByName('parole')[1].value;
	if (!/^\s*$/.test(value)) {
		return true;
	}

	alert("Devi inserire almeno una parola da cercare");
	return false;
}