function generatePOS() {
    var results = []
    let startingSem = document.querySelector('#select-semester').innerHTML;
    results.push(startingSem);
    let numberSem = document.querySelector('#number-of-semester').innerHTML;
    results.push(numberSem);
    let campus = document.querySelector('#select-campus').innerHTML;
    results.push(campus);
    let concentration = document.querySelector('#concentration').innerHTML;
    results.push(concentration);
    let modality = document.querySelector('#modality').innerHTML;
    results.push(modality);
    let waiver = document.querySelector('#waiver').innerHTML;
    results.push(waiver);

    return results;
}

function validateForm() {
    if (document.generateForm.semester.value === "" ||
        document.generateForm.no_of_semester.value === "" ||
        document.generateForm.campus.value === "" ||
        document.generateForm.concentration.value === "" ||
        // document.generateForm.coures_modality.value === "" ||
        document.generateForm.waiver.value === ""
    ) {
        alert("Please Fill all the Options")
        return false;
    }
    return true
}

function semester_choice(key_pressed) {
    const val = document.getElementById(key_pressed.id).dataset.value;
    document.getElementById('select-semester').innerHTML = val;
    document.generateForm.semester.value = val;
}

function year(key_pressed1) {
    const val1 = document.getElementById(key_pressed1.id).dataset.value;
    document.getElementById('year').innerHTML = val1;
    document.generateForm.year.value = val1;
}

function no_semester(key_pressed1) {
    const val1 = document.getElementById(key_pressed1.id).dataset.value;
    document.getElementById('number-of-semester').innerHTML = val1;
    document.generateForm.no_of_semester.value = val1;
}

function campus(key_pressed2) {
    const val2 = document.getElementById(key_pressed2.id).dataset.value;
    document.getElementById('select-campus').innerHTML = val2;
    document.generateForm.campus.value = val2;
}

function concentration_selection(key_pressed) {
    const val2 = document.getElementById(key_pressed.id).dataset.value;
    document.getElementById('concentration').innerHTML = val2;
    document.generateForm.concentration.value = val2;
}

function modality(key_pressed) {
    const val2 = document.getElementById(key_pressed.id).dataset.value;
    document.getElementById('modality').innerHTML = val2;
    document.generateForm.coures_modality.value = val2;
}

function waiver(key_pressed) {
    const val2 = document.getElementById(key_pressed.id).dataset.value;
    document.getElementById('waiver').innerHTML = val2;
    document.generateForm.waiver.value = val2;
}
