from django.db import models
from django.conf import settings


class AcademicRule(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to="academic_rules/")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Lecturer(models.Model):
    TITLE_CHOICES = [
        ('Mr', 'Mr'),
        ('Ms', 'Ms'),
        ('Dr', 'Dr'),
        ('Prof', 'Prof'),
    ]
    
    LECTURER_TYPE_CHOICES = [
        ('Junior Lecturer', 'Junior Lecturer'),
        ('Lecturer', 'Lecturer'),
        ('Senior Lecturer', 'Senior Lecturer'),
        ('Associate Professor', 'Associate Professor'),
        ('Professor', 'Professor'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, choices=TITLE_CHOICES, default='Mr')
    bio = models.TextField(help_text="The full biography for the main content area.")
    short_bio = models.TextField(blank=True, help_text="A brief summary for the profile header.")
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    office = models.CharField(max_length=100)
    consultation_hours = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20)
    lecturer_type = models.CharField(max_length=20, choices=LECTURER_TYPE_CHOICES, default='Lecturer')
    joined_year = models.IntegerField()
    expertise_areas = models.TextField(help_text="Comma-separated list of expertise areas.")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Qualification(models.Model):
    FORMAT_CHOICES = [
        ('Contact', 'Contact'),
        ('Distance', 'Distance'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration_years = models.IntegerField()
    total_credits = models.IntegerField()
    total_modules = models.IntegerField()
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='Contact')

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)
    description = models.TextField()
    credits = models.IntegerField()
    year = models.IntegerField()
    semester = models.IntegerField()
    lecturers = models.ManyToManyField(Lecturer)
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='prerequisite_for')
    corequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='corequisite_for')

    def __str__(self):
        return f"{self.code} - {self.name}"


class LearningOutcome(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='learning_outcomes')
    description = models.TextField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.module.code} - Learning Outcome {self.id}"


class QualificationModule(models.Model):
    MODULE_TYPE_CHOICES = [
        ('Core', 'Core'),
        ('Auxiliary', 'Auxiliary'),
    ]
    
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    module_type = models.CharField(max_length=20, choices=MODULE_TYPE_CHOICES)

    def __str__(self):
        return f"{self.qualification.name} - {self.module.code}"


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_number = models.CharField(max_length=20)
    qualification = models.ForeignKey(Qualification, on_delete=models.SET_NULL, null=True, blank=True)
    current_year = models.IntegerField(null=True, blank=True)
    current_semester = models.IntegerField(null=True, blank=True)
    completed_modules = models.ManyToManyField(Module, blank=True)

    def __str__(self):
        return f"{self.student_number} - {self.user.get_full_name()}"