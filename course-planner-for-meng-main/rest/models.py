from django.db import models

# Create your models here.
class Course(models.Model):
    course_number = models.CharField(max_length=10)
    course_name = models.CharField(max_length=100)
    DEPT_CHOICES = (
            ('CS','Computer Science'),
            ('ECE','Computer Engineering'),
            ('STAT','Statistics'),
            ('MATH','Math'),
            ('CEE','Civil and Environmental Engineering'),
            ('BIT','Business Information Technology'),
            ('BCHM','Biochemistry'),
            ('AOE','Aerospace and Ocean Engineering'),
            ('ACIS','Accounting and Information Systems'),
            ('ME','Mechanical Engineering'),
            ('PHIL','Philosophy'),
            ('PPWS','Plant Pathology, Physiology, & Weed Science'),
            ('STS','Science and Technology Studies'),
            ('EDRE','Educational Research and Evaluation'),
            ('ESM','Engineering Science and Mechanics'),
            ('GEOG','Geography'),
            ('ISE','Industrial Systems Engineering'),
            )
    department = models.CharField(choices = DEPT_CHOICES, blank=True, null=True, max_length=100)
    # TERM_CHOICES = (
    #     ('Fall','Fall'),
    #     ('Spring','Spring'),
    #     ('Summer','Summer'),
    #     ('Winter','Winter')
    # )
    # term_offering = models.CharField(choices = TERM_CHOICES, blank=True, null=True, max_length=100)
    term_offering = models.CharField(blank=True, null=True, max_length=100)
    
    # CAMPUS_CHOICES = (
    #     ('Blacksburg','Blacksburg'),
    #     ('NCR','NCR'),
    #     ('Virtual Campus','Virtual')
    # )
    # campus = models.CharField(choices = CAMPUS_CHOICES, blank=True, null=True, max_length=100)
    campus = models.CharField(blank=True, null=True, max_length=100)
    
    # MODALITY_CHOICES = (
    #     ('Face2Face','Face2Face'),
    #     ('Hybrid','Hybrid'),
    #     ('Online','Online'),
    #     ('Online Synchronous','Online Synchronous'),
    #     ('Online Asynchronous','Online Asynchronous'),
    # )
    # modality = models.CharField(choices = MODALITY_CHOICES, blank=True, null=True, max_length=100)
    modality = models.CharField(blank=True, null=True, max_length=100)
    
    course_description = models.TextField(blank=True, null=True)
    course_website = models.URLField(max_length=200, blank=True, null=True)
    faculty = models.CharField(max_length=100, blank=True, null=True)
    prerequisite_courses = models.ForeignKey('Course', blank=True, null=True, on_delete=models.SET_NULL)
    prerequisite_concepts = models.CharField(max_length=200, blank=True, null=True)
    concentration = models.ForeignKey('Concentration', blank=True, null=True, on_delete=models.SET_NULL)
    learning_objective = models.TextField(max_length = 200, blank=True, null=True)
    syllabus = models.URLField(max_length=200,blank=True, null = True)
    credit_hours = models.IntegerField(blank=True, null=True)
    special_study = models.BooleanField(blank=True, null=True, default=False)
    cognate_course = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self) -> str:
        if self.department:
            return self.department + " " + self.course_number +" "+ self.course_name
        return self.course_number +" "+ self.course_name
        
    class Meta:
        ordering = ("id",)
    


class Concentration(models.Model):
    names = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.names

    class Meta:
        ordering = ("id",)

class DegreeRequirement(models.Model):
    CRITERIA_CHOICES = (
        ('C', 'Concentration'),
        ('Co', 'Cognate'),
        ('M','Mandatory Course')
    )
    criteria = models.CharField(choices = CRITERIA_CHOICES,max_length=100)
    course = models.ForeignKey('Course',blank=True, null=True, on_delete=models.CASCADE)
    COMPARATOR_CHOICES = (
        ('AL','At least'),
        ('AM','At most')
    )
    comparator = models.CharField(choices = COMPARATOR_CHOICES,blank=True, null=True, max_length=100)
    waivable = models.BooleanField()
    value = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ("id",)

# Course - 
#     Id - auto generated
#     Course Request Number - Number
#     Course Number - text
#     Course Name - text
#     Department - text
#     Term Offering - Fall/Spring/Summer (Multiselect)
#     Campus - Blacksburg/NCR/Virtual (Multiselect)
#     Modality - Online Asynchronous/Online Synchronous/Hybrid/F2F
#     Course Description - text
#     Course Website - text
#     Faculty - text
#     Prerequisite Courses - Foreign Key
#     Prerequisite Concepts - text
#     Concentration - Foreign Key
#     Learning Objective - text
#     Syllabus - blob file
#     Credit Hours - number
#     Special Study - boolean
#     Cognate Course - boolean

# Concentration - 
#     Id - auto generated
#     Name - text

# Degree Requirements - 
#     Id - auto generated
#     Criteria - Concentration/Cognate/Mandatory Course
#     Course - Foreign Key
#     Comparator - At Least/At Most
#     Waivable - Boolean
#     Value - Number
