function generatePOS() {
    let startingSem = document.querySelector('#startingSem').value;
    let courseNumber = document.querySelector('#courseNumber').value;
    let courseName = document.querySelector('#courseName').value;
    let campus = document.querySelector('#campus').value;
    let concentration = document.querySelector('#concentration').value;
    let modality = document.querySelector('#modality').value;

    var request = {
        "startingSem": startingSem,
        "courseNumber": courseNumber,
        "courseName": courseName,
        "campus": campus,
        "concentration": concentration,
        "modality": modality
    };

    $.ajax({
        url: "/rest/search",
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
    if(document.generateForm.semester.value === "" ||
    document.generateForm.course_number.value === "" ||
    document.generateForm.course_name.value === "" ||
    document.generateForm.campus.value === "" ||
    document.generateForm.concentration.value === "" ||
    document.generateForm.coures_modality.value === "" 
    )

    //  {
    //     alert("Please Fill all the Options")
    //     return false;
    // }
    return true
}
