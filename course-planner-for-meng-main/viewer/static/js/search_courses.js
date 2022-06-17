function filterSearch() {
    
    let course_number = document.querySelector('#course_number').value;
    console.log("entered here");

    var request = {
        "course_number": course_number,
        
    };

    $.ajax({
        url: "/search_results",
        dataType: "json",
        data: requelst,
        type: "GET",
        
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
    if(document.generateForm.concentration.value === ""
    
    ) {
        alert("Please Fill all the Options")
        return false;
    }
    return true
}