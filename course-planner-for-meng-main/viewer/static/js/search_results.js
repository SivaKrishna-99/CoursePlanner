function generatePOS() {
    let startingSem = document.querySelector('#startingSem').value;
    let courseNumber = document.querySelector('#courseNumber').value;
    let courseName = document.querySelector('#courseName').value;
    let campus = document.querySelector('#campus').value;
    let concentration = document.querySelector('#concentration').value;
    let modality = document.querySelector('#modality').value;

    var request = {
        "term_offering": startingSem,
        "course_number": courseNumber,
        "course_name": courseName,
        "campus": campus,
        "concentration": concentration,
        "modality": modality
    };

    $.ajax({
        url: "/rest/search_results",
        dataType: "json",
        data: request,
        type: "POST",
        
        success: function (response) {
            console.log("success");
            console.log(JSON.stringify(response));
        },
        error: function (response) {
            console.log("error");
            console.log(JSON.stringify(response))
        }
    })
}

function validateForm() {
    
    return true
}
