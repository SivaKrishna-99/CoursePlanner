from django.contrib import admin
from rest.models import Course,Concentration,DegreeRequirement

# Register your models here.
# admin.site.register(Course)
# admin.site.register(Concentration)
# admin.site.register(DegreeRequirement)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("department", "course_number", "course_name","term_offering", "campus", "modality", "concentration", "prerequisite_courses")
    list_filter = ("concentration", "department", "campus", "modality")

@admin.register(Concentration)
class ConcentrationAdmin(admin.ModelAdmin):
    list_display = ("id", "names")

@admin.register(DegreeRequirement)
class DegreeRequirementAdmin(admin.ModelAdmin):
    list_display = ("id", "criteria", "course", "comparator", "waivable", "value")
    # list_filter = ("department", "campus", "modality")