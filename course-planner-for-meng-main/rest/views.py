from multiprocessing.connection import wait
from time import sleep
from django.http import HttpResponse
from django.shortcuts import render
from rest.models import Concentration, Course, DegreeRequirement
from itertools import chain
import json
import os
from fillpdf import fillpdfs
from django.db.models import Q

# Create your views here.
def select_courses(request):
    return render(request, 'select_courses.html', {})

def search_results(request):
    return render(request, 'search_results.html', {})

def search_rest():
    context ={}
    #Getting the information from Course table 
    courses = Course.objects.all().order_by()
    #values_list returns a QuerySet containing tuples (flat = true returns a single value instead of 1-tuples)
    course_numbers = courses.values_list('course_number',flat=True).distinct()
    course_name = courses.values_list('course_name',flat=True).distinct()
    modality = courses.values_list('modality',flat=True).distinct()
    term_offering = courses.values_list('term_offering',flat=True).distinct()
    campus = courses.values_list('campus',flat=True).distinct()
    concentrations = Concentration.objects.values_list('names',flat=True)
    
    context['course_numbers'] = course_numbers
    context['course_names'] = course_name
    context['modality'] = modality
    context['campus'] = campus
    context['term_offering'] = term_offering
    context['concentrations'] = concentrations
    
    return context



#Getting search results
def search_res(request):
    
    context = {}
    #objects.all() returns a queryset
    courses = Course.objects.all()
    #request contains the info fro the user ,GET is the address of the webpage and get() method is used to perform operation on dictionary 
    course_number = request.GET.get("course_number",None)
    course_name = request.GET.get("course_name",None)
    campus = request.GET.get("campus",None)
    term_offering = request.GET.get("term_offering",None)
    concentration = request.GET.get("concentration",None)
    modality = request.GET.get("course_modality",None)
    
    if course_number:
        courses = courses.filter(course_number = course_number)
    
    if course_name:
        courses = courses.filter(course_name = course_name)
    
    if term_offering:
        courses = courses.filter(term_offering__contains = term_offering)
        
    if campus:
        courses = courses.filter(campus__contains = campus)
    
    
    if concentration:
        con_name = Concentration.objects.get(id =concentration).names  
        con_objects = Concentration.objects.all().order_by()
        concen_ids = con_objects.filter(names__contains = con_name).values_list('id',flat=True).distinct() 
        courses = courses.filter(concentration_id__in = concen_ids)
          
        
    if modality:
        courses = courses.filter(modality__contains = modality)
    
    return courses

#Getting Course details
def search_course_detail(request,course_name):
    
    course = Course.objects.get(course_name = course_name)
    context = {}
    context['modality'] = course.modality
    context['course_number'] = course.course_number
    context['course_name'] = course.course_name
    context['description'] = course.course_description
    context['syllabus'] = course.syllabus
    context['term_offering'] = course.term_offering
    context['faculty'] = course.faculty
    
    if course.concentration_id :
        concentration = Concentration.objects.get(id = course.concentration_id)
        context['concentration'] = concentration.names
    else:
        context['concentration'] = None
    
    if course.prerequisite_courses_id:
        courses = Course.objects.all().order_by()
        preq = courses.filter(id = course.prerequisite_courses_id)
        context['preq'] = preq.order_by().values_list('course_name',flat=True).distinct()
    else:
        context['preq'] = None
    return context


#search courses
def search(request):
    
    courses = Course.objects.all()
    course_number= request.GET.get("course_number")
    course_name = request.GET.get("course_name")
    term_offering = request.GET.get("term_offering")
    campus = request.GET.get("campus")
    concentration = request.GET.get("concentration")
    modality = request.GET.get("modality")
    
    context = {}


    if course_number:
        courses = courses.filter(course_number=course_number)
        
    if course_name:
        courses = courses.filter(course_name=course_name)
        
    if term_offering:
        courses = courses.filter(term_offering = term_offering)
        
    if campus:
        courses = courses.filter(campus = campus)
        
    if concentration:
        courses = courses.filter(concentration =  concentration)
        
    if modality:
        courses = courses.filter(modality = modality)
    
    context["courses"] = courses
    
    return render(request, 'search.html', context)

def choose_courses_rest(semester, year, no_semesters, campus, concentration, modality, cs5040waiver):
    mandatory_courses = list(Course.objects.filter(degreerequirement__criteria="M").values("id", "course_number","course_name","term_offering", "campus", "modality", "special_study", "prerequisite_courses__course_name","prerequisite_courses__course_number","cognate_course","department"))
    concentration_courses = list(Course.objects.filter(concentration__names=concentration).values("id", "course_number","course_name","term_offering", "campus", "modality", "special_study", "prerequisite_courses__course_name","prerequisite_courses__course_number","cognate_course","department"))
    
    if campus == "Virtual":
        print(campus)
        allCoursesQuerySet = Course.objects.filter(Q(campus__icontains=campus) | Q(modality__icontains='Online') | Q(modality=''))
    else :
        allCoursesQuerySet = Course.objects.filter(Q(campus__icontains=campus) | Q(campus='') | Q(campus__icontains='Virtual'))

    all_courses = list(allCoursesQuerySet.values("id", "course_number","course_name","term_offering", "campus", "modality", "special_study", "prerequisite_courses__course_name","prerequisite_courses__course_number","cognate_course","department"))

    semesters = [semester]
    years = [int(year)]
    semesterYears = [semesters[-1] + " " + str(years[-1])]
    for i in range(int(no_semesters)-1):
        years.append(int(years[-1]) if semesters[-1]=="Spring" else int(years[-1])+1)
        semesters.append("Fall" if semesters[-1]=="Spring" else "Spring")
        semesterYears.append(semesters[-1] + " " + str(years[-1]))

    context = {}
    context['mandatory_courses'] = mandatory_courses
    context['concentration_courses'] = concentration_courses
    context['all_courses'] = all_courses
    context['semester_count'] = no_semesters
    context['semester'] = semester
    context['semesters'] = semesters
    context['year'] = year
    context['years'] = years
    context['semesterYears'] = semesterYears
    context['max_courses_per_sem'] = range(1,6)
    context['waiver'] = cs5040waiver

    return context


def courses_summary(selectedCoursesMap):
    semesterCourses = []
    concentrationCounts = {}
    concentrations = []
    cognateCounts = 0
    errors = []
    minConcentrationCount = DegreeRequirement.objects.values("value").get(criteria="C")['value']
    maxCognateCount = DegreeRequirement.objects.values("value").get(criteria="Co")['value']
    selectedCourseIdMap={}
    hasWaiver = False

    if selectedCoursesMap==None or len(selectedCoursesMap.keys()) == 0:
        concentration_courses = list(Course.objects.filter(concentration__names="Software Development and Applications").values("course_number","course_name","department","concentration__names")[:4])
        all_courses = list(Course.objects.all().values("course_number","course_name","department","concentration__names")[:6])
        semesterCourses=concentration_courses+all_courses

    else:
        for key in selectedCoursesMap.keys():
            if key == 'waiver':
                hasWaiver = selectedCoursesMap[key] == "Yes"
                continue
            semYear = key.split('_')[-1]
            entry = {}
            entry['semYear'] = semYear
            entry['sem'] = semYear.split(' ')[0]
            entry['year'] = semYear.split(' ')[-1]
            entry['course'] = Course.objects.values("id", "course_number","course_name","department","concentration__names","cognate_course",'prerequisite_courses__id','prerequisite_courses__course_name',
                    'prerequisite_courses__course_number', 'prerequisite_courses__department').get(pk=selectedCoursesMap[key])
            selectedCourseIdMap[entry['course']['id']] = True
            if entry['course']['prerequisite_courses__id']:
                preReqSatisfied = False
                for e in semesterCourses:
                    if e['course']['id'] == entry['course']['prerequisite_courses__id']:
                        preReqSatisfied = e['semYear'] != entry['semYear']
                        break
                if not preReqSatisfied:
                    errors.append(entry['course']['department'] + entry['course']['course_number'] + ' ' + entry['course']['course_name'] + 
                                ' has a prerequisite of ' +
                                entry['course']['prerequisite_courses__department'] + entry['course']['prerequisite_courses__course_number'] + ' ' + entry['course']['prerequisite_courses__course_name']
                    )
            semesterCourses.append(entry)

    for entry in semesterCourses:
        if entry['course']['cognate_course']:
            cognateCounts = cognateCounts + 1
        if entry['course']['concentration__names']:
            if entry['course']['concentration__names'] not in concentrationCounts.keys():
                concentrationCounts[entry['course']['concentration__names']] = 1
            else:
                concentrationCounts[entry['course']['concentration__names']] = concentrationCounts[entry['course']['concentration__names']] + 1

    for c in concentrationCounts.keys():
        if concentrationCounts[c] >= minConcentrationCount:
            concentrations.append(c)

    degReq = list(DegreeRequirement.objects.values("criteria","comparator","waivable","value","course__id","course__department","course__course_number","course__course_name").all())

    for dg in degReq:
        if dg['criteria'] == 'M':
            if dg['course__id'] not in selectedCourseIdMap.keys():
                if not dg['waivable']:
                    errors.append('Mandatory Course '+ dg['course__department'] + dg['course__course_number'] + ' ' + dg['course__course_name'] + ' not satisfied.')
                else:
                    if not hasWaiver:
                        errors.append('Mandatory Course '+ dg['course__department'] + dg['course__course_number'] + ' ' + dg['course__course_name'] + ' not satisfied.')
        if dg['criteria'] == 'C':
            if len(concentrations) == 0:
                errors.append("Less than " + str(minConcentrationCount) + " concentration courses taken. Minimum " + str(minConcentrationCount) + " required in any concentration area.")
        if dg['criteria'] == 'Co':
            if cognateCounts > maxCognateCount:
                errors.append(str(cognateCounts) + " cognate courses taken. Maximum " + str(maxCognateCount) + " cognate courses can be taken.")

    context = {}
    context['courses'] = semesterCourses
    if(len(errors) > 0):
        context['errors'] = errors
    context['concentrations'] = concentrations
    context['waiver'] = hasWaiver
    return context

def generatePOSpdf(data):
    courses = data['courses']
    concentration = data['concentration']
    waiver = data['waiver']

    data_dict = {}
    if waiver:
        data_dict['Waived Checkbox'] = waiver
    
    concentrationCount = 0
    undergradCount = 0
    gradCount = 0

    for c in courses:
        # Find DSA Course
        if c['course']['course_number'] == '5040' and c['course']['department'] == 'CS':
            data_dict['Semester 1'] = c['sem']
            data_dict['Year 1'] = c['year']
            data_dict['Credits 1'] = 3
            continue
        
        # Find Ethics Course
        if c['course']['course_number'] == '5024' and c['course']['department'] == 'CS':
            data_dict['Semester 2'] = c['sem']
            data_dict['Year 2'] = c['year']
            data_dict['Credits 2'] = 3
            continue
        
        # Find Capstone course
        if c['course']['course_number'] == '5934' and c['course']['department'] == 'CS':
            data_dict['Semester 3'] = c['sem']
            data_dict['Year 3'] = c['year']
            data_dict['Credits 3'] = 3
            continue

        # Concentration Courses
        if c['course']['concentration__names'] == concentration and concentrationCount < 3:
            concentrationCount = concentrationCount + 1
            data_dict['Concentration Area '+str(concentrationCount)] = concentration
            data_dict['Course Number '+str(concentrationCount)] = c['course']['department']+c['course']['course_number']
            data_dict['Course Name '+str(concentrationCount)] = c['course']['course_name']
            data_dict['Semester '+str(concentrationCount+3)] = c['sem']
            data_dict['Year '+str(concentrationCount+3)] = c['year']
            data_dict['Credits '+str(concentrationCount+3)] = 3
            continue

        # 4000 level courses
        if int(c['course']['course_number']) < 5000 and undergradCount < 3:
            undergradCount = undergradCount + 1
            data_dict['Course Number '+str(undergradCount + 8)] = c['course']['department']+c['course']['course_number']
            data_dict['Course Name '+str(undergradCount + 8)] = c['course']['course_name']
            data_dict['Semester '+str(undergradCount+8+3)] = c['sem']
            data_dict['Year '+str(undergradCount+8+3)] = c['year']
            data_dict['Credits '+str(undergradCount+8+3)] = 3
            continue

        # 5000 level or higher courses
        if int(c['course']['course_number']) > 5000 and gradCount < 5:
            gradCount = gradCount + 1
            data_dict['Course Number '+str(gradCount + 3)] = c['course']['department']+c['course']['course_number']
            data_dict['Course Name '+str(gradCount + 3)] = c['course']['course_name']
            data_dict['Semester '+str(gradCount+3+3)] = c['sem']
            data_dict['Year '+str(gradCount+3+3)] = c['year']
            data_dict['Credits '+str(gradCount+3+3)] = 3
            continue

    path = 'new.pdf'

    fillpdfs.write_fillable_pdf('PlanMEng.pdf', path, data_dict)

    with open(path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="text/csv", charset="utf-8")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(path)
        return response
