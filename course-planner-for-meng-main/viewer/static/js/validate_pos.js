function downloadPOS() {
    data = {
        courses: courses_selected,
        concentration: document.getElementById('concentration').value,
        waiver: waiver
    }
    fetch("downloadPOS", {
        body: JSON.stringify(data),
        method: 'POST',
        headers: {
            'Content-Type': 'application/json; charset=utf-8',
            'X-CSRFToken': Cookies.get('csrftoken')
        },
    })
    .then(response => {
        if(!response.ok) {
            alert("Something went wrong :(")
            return
        }
        return response.blob()
    })
    .then(response => {
        if(response) {
            const blob = new Blob([response], {type: 'application/pdf'});
            const downloadUrl = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = downloadUrl;
            a.download = "PlanMEng.pdf";
            document.body.appendChild(a);
            a.click();
        }
    })

    // $.ajax({
    //     url:"downloadPOS",
    //     type: "POST",
    //     headers: {'X-CSRFToken': Cookies.get('csrftoken')},
    //     data: {'coursesSelected': JSON.stringify(courses_selected)},
    //     // what to do when the call is success 
    //     success:function(data){
    //         console.log("success");
    //         console.log(JSON.stringify(data));
    //     },
    //     // what to do when there is an error
    //     error:function (xhr, textStatus, thrownError){
    //         console.log("error");
    //     }
    // });
}