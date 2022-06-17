var coursesToDisplay = []
var coursesToDisplayMap = {}
var coursesSelected = {}
var allCoursesOrdered = []

window.onload = function() {
    allCoursesOrdered = concentration_courses.concat(mandatory_courses,all_courses)

    formOptions()

    allCoursesOrdered = JSON.parse(JSON.stringify(coursesToDisplay))

    springCourses = coursesToDisplay.filter(function(e) {return e.term_offering == null || e.term_offering == '' || e.term_offering.includes('Spring')})
    fallCourses = coursesToDisplay.filter(function(e) {return e.term_offering == null || e.term_offering == '' || e.term_offering.includes('Fall')})

    var springStr = "<option selected='selected' value='' disabled>Select a Course</option>"
    for(var course of springCourses) {
        springStr += `<option value="${course.id}">${course.department+course.course_number +' '+ course.course_name}</option>`
    }

    var fallStr = "<option selected='selected' value='' disabled>Select a Course</option>"
    for(var course of fallCourses) {
        fallStr += `<option value="${course.id}">${course.department+course.course_number +' '+ course.course_name}</option>`
    }

    for(let i=1; i<=semester_count; i++ ) {
        let sY = semesterYears[i-1]
        let term = sY.split(' ')[0]
        for(let j=1; j<=5; j++) {
            document.getElementById(`${i}_${j}_${sY}`).innerHTML = term === 'Spring' ? springStr : fallStr;
        }
    }
};

function formOptions() {
    coursesToDisplay = []
    for(let i=0; i<allCoursesOrdered.length; i++ ) {
        if(!(allCoursesOrdered[i].id in coursesToDisplayMap)) {
            coursesToDisplay.push(JSON.parse(JSON.stringify(allCoursesOrdered[i])))
            coursesToDisplayMap[allCoursesOrdered[i].id] = allCoursesOrdered[i]
        }
    }
}

function updateCoursesToDisplay() {
    coursesToDisplay = []
    for(let i=0; i<allCoursesOrdered.length; i++ ) {
        if((allCoursesOrdered[i].id in coursesToDisplayMap)) {
            coursesToDisplay.push(JSON.parse(JSON.stringify(allCoursesOrdered[i])))
        }
    }
}

function updatePicklists(sem,course, semYear) {
    let selectedCourseNumber = document.getElementById(`${sem}_${course}_${semYear}`).value;
    let key=sem+'-'+course
    
    var oldCourse = key in coursesSelected ? coursesSelected[key] : null
    var newCourse = coursesToDisplayMap[selectedCourseNumber]
    
    if(oldCourse!= null && oldCourse.id === newCourse.id) {
        return
    }
    
    coursesSelected[key] = JSON.parse(JSON.stringify(newCourse))
    // document.selectCoursesForm.selected_courses.value = JSON.stringify(coursesSelected);

    
    delete(coursesToDisplayMap[selectedCourseNumber])
    if(oldCourse != null) {
        coursesToDisplayMap[oldCourse.id] = oldCourse
    }

    updateCoursesToDisplay()
    // coursesToDisplay = coursesToDisplay.filter(function(e) {return e.id !== selectedCourseNumber})

    springCourses = coursesToDisplay.filter(function(e) {return e.term_offering == null || e.term_offering == '' || e.term_offering.includes('Spring')})
    fallCourses = coursesToDisplay.filter(function(e) {return e.term_offering == null || e.term_offering == '' || e.term_offering.includes('Fall')})

    var springStr = ""
    for(var course of springCourses) {
        springStr += `<option value="${course.id}">${course.department+course.course_number +' '+ course.course_name}</option>`
    }

    var fallStr = ""
    for(var course of fallCourses) {
        fallStr += `<option value="${course.id}">${course.department+course.course_number +' '+ course.course_name}</option>`
    }

    // var str=""
    // for(let course of coursesToDisplay) {
    //     str += `<option value="${course.id}">${course.department+course.course_number +' '+ course.course_name}</option>`
    // }

    for(let i=1; i<=semester_count; i++ ) {
        let sY = semesterYears[i-1]
        let term = sY.split(' ')[0]
        let str = term === 'Spring' ? springStr : fallStr;
        for(let j=1; j<=5; j++) {
            let key=i+'-'+j
            if(key in coursesSelected) {
                let selectedCourse = coursesSelected[key]
                document.getElementById(`${i}_${j}_${sY}`).innerHTML = `<option selected='selected' value="${selectedCourse.id}">${selectedCourse.department+selectedCourse.course_number +' '+ selectedCourse.course_name}</option>` + str;
                // document.getElementById(`sem${i}_course${j}`).value = selectedCourse.id
            } else {
                document.getElementById(`${i}_${j}_${sY}`).innerHTML = "<option selected='selected' value='' disabled>Select a Course</option>" + str;
            }
        }
    }
};

function validateForm() {
    if (Object.keys(coursesSelected).length < 10) {
        alert("Please Select at least 10 courses")
        return false;
    }
    return true
}