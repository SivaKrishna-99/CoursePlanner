from operator import mod
from django.shortcuts import render
from rest.views import search_rest,search_res,search_course_detail,choose_courses_rest,courses_summary,generatePOSpdf
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def index(request):
    return render(request, 'index.html')

def valid(request):
    courses = courses_summary(request.GET)
    return render(request, 'valid_pos.html', context = courses)


def summary(request):
    courses = courses_summary(request.GET)
    return render(request, 'summary.html', context = courses)

def select_courses(request):
    semester = request.GET.get("semester")
    year = request.GET.get("year")
    no_semesters = request.GET.get("no_of_semester")
    campus = request.GET.get("campus")
    concentration = request.GET.get("concentration")
    modality = request.GET.get("coures_modality")
    cs5040waiver = request.GET.get("waiver")
    
    courses = choose_courses_rest(semester, year, no_semesters, campus, concentration, modality, cs5040waiver)

    return render(request, 'select_courses.html', context=courses)

def search_courses(request):
    context = search_rest()
    return render(request, 'search_courses.html', context)

def search_detail(request,course_name):
    context = search_course_detail(request,course_name)
    return render(request, 'search_detail.html',context)

def search_results(request):
    courses = search_res(request)
    return render(request, 'search_results.html',{'courses':courses})

def about(request):
    return render(request, 'about.html')

@csrf_exempt
def downloadPOS(request):
    return generatePOSpdf(json.loads(request.body.decode("utf-8")))
    # return render(request, 'about.html')
