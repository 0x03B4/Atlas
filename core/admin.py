from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    Student,
    Qualification,
    Module,
    Lecturer,
    QualificationModule,
    AcademicRule,
    LearningOutcome 
)

class LearningOutcomeInline(admin.TabularInline):
    model = LearningOutcome
    extra = 3

class ModuleAdmin(admin.ModelAdmin):
    inlines = [LearningOutcomeInline]
    list_display = ('code', 'name', 'year', 'semester', 'credits')
    search_fields = ('name', 'code')

class QualificationAdmin(ImportExportModelAdmin):
    list_display = ('name', 'duration_years', 'total_credits', 'format') 

admin.site.register(Student)
admin.site.register(Qualification, QualificationAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lecturer)
admin.site.register(QualificationModule)
admin.site.register(AcademicRule)