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
    
    QUALIFICATION_CHOICES = [
        ('BSc', 'BSc'),
        ('Hons', 'Hons'),
        ('MSc', 'MSc'),
        ('PhD', 'PhD'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, choices=TITLE_CHOICES, default='Mr')
    bio = models.TextField(help_text="The full biography for the main content area.")
    short_bio = models.TextField(blank=True, help_text="A brief summary for the profile header.")
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    office = models.CharField(max_length=100, blank=True)
    consultation_hours = models.CharField(max_length=100, blank=True)
    employee_id = models.CharField(max_length=20, unique=True)
    lecturer_type = models.CharField(max_length=20, choices=LECTURER_TYPE_CHOICES, default='Lecturer')
    joined_year = models.IntegerField()
    expertise_areas = models.TextField(help_text="Comma-separated list of expertise areas.")
    highest_qualification = models.CharField(max_length=10, choices=QUALIFICATION_CHOICES, default='MSc', blank=True)
    estimated_student_count = models.PositiveIntegerField(default=100, help_text="Estimated number of students taught.")

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"

    def get_expertise_areas_list(self):
        return [a.strip() for a in self.expertise_areas.split(',') if a.strip()]


class Qualification(models.Model):
    FORMAT_CHOICES = [
        ('Contact', 'Contact'),
        ('Distance', 'Distance'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration_years = models.PositiveIntegerField()
    total_credits = models.PositiveIntegerField()
    total_modules = models.PositiveIntegerField()
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='Contact')

    def __str__(self):
        return self.name

    @property
    def semesters(self):
        return self.duration_years * 2

    def get_modules_by_year_and_semester(self):
        modules_by_year = {}
        qualification_modules = (
            self.qualificationmodule_set
            .select_related('module')
            .order_by('module__year', 'module__semester')
        )
        for qm in qualification_modules:
            year, semester = qm.module.year, qm.module.semester
            if year not in modules_by_year:
                modules_by_year[year] = {1: [], 2: []}
            modules_by_year[year][semester].append(qm)
        return dict(sorted(modules_by_year.items()))


class Module(models.Model):
    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
    ]
    
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    credits = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    semester = models.PositiveIntegerField(choices=SEMESTER_CHOICES, default=1)
    lecturers = models.ManyToManyField(Lecturer, related_name='modules', blank=True)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='prerequisite_for')
    corequisites = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='corequisite_for')

    def __str__(self):
        return f"{self.code} - {self.name}"


class LearningOutcome(models.Model):
    module = models.ForeignKey(Module, related_name='learning_outcomes', on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.module.code}: {self.description[:50]}..."


class QualificationModule(models.Model):
    MODULE_TYPE_CHOICES = [
        ('Core', 'Core'),
        ('Auxiliary', 'Auxiliary'),
    ]
    
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    module_type = models.CharField(max_length=20, choices=MODULE_TYPE_CHOICES)

    def __str__(self):
        return f"{self.qualification.name} - {self.module.code} ({self.module_type})"


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_number = models.CharField(max_length=20, unique=True)
    qualification = models.ForeignKey(Qualification, on_delete=models.SET_NULL, null=True, blank=True)
    current_year = models.PositiveIntegerField(null=True, blank=True)
    current_semester = models.PositiveIntegerField(null=True, blank=True)
    completed_modules = models.ManyToManyField(Module, blank=True)

    def __str__(self):
        return f"{self.student_number} - {self.user.get_full_name()}"

 
    
    def get_dashboard_context(self):
        if not all([self.qualification, self.current_year, self.current_semester]):
            return None

        qualification = self.qualification

        current_modules_count = qualification.qualificationmodule_set.filter(
            module__year=self.current_year,
            module__semester=self.current_semester
        ).count()

        module_distribution = {
            year: qualification.qualificationmodule_set.filter(module__year=year).count()
            for year in range(1, qualification.duration_years + 1)
        }

        academic_progress = {}
        total_credits_earned = 0
        
        # A module is considered "completed" if its year is less than the student's current year,
        # OR if it's in the current year but a past semester.
        # This is an assumption. For a real-world app, you'd have a more robust system
        # (e.g., linking to grades or an explicit 'completed' status).
        completed_modules_qs = qualification.qualificationmodule_set.filter(
            models.Q(module__year__lt=self.current_year) |
            (models.Q(module__year=self.current_year) & models.Q(module__semester__lt=self.current_semester))
        ).select_related('module')

        for year in range(1, qualification.duration_years + 1):
            total_modules_in_year = qualification.qualificationmodule_set.filter(module__year=year).select_related('module')
            completed_modules_in_year = completed_modules_qs.filter(module__year=year)
            
            credits_earned_in_year = sum(qm.module.credits for qm in completed_modules_in_year)
            total_credits_in_year = sum(qm.module.credits for qm in total_modules_in_year)
            total_credits_earned += credits_earned_in_year

            status = 'Future'
            if year < self.current_year:
                status = 'Completed'
            elif year == self.current_year:
                status = 'In Progress'

            academic_progress[year] = {
                'status': status, 'credits_earned': credits_earned_in_year, 'total_credits': total_credits_in_year, 
                'percentage': (credits_earned_in_year / total_credits_in_year) * 100 if total_credits_in_year > 0 else 0
            }

        credits_remaining = qualification.total_credits - total_credits_earned
        overall_progress = round((total_credits_earned / qualification.total_credits) * 100) if qualification.total_credits > 0 else 0

        return {
            'student': self, 'current_modules_count': current_modules_count, 'module_distribution': module_distribution,
            'academic_progress': academic_progress, 'total_credits_earned': total_credits_earned, 
            'credits_remaining': credits_remaining, 'overall_progress': overall_progress,
        }