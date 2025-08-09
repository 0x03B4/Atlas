from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Qualification, Module, Lecturer, AcademicRule


from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def programs_view(request):
    search_query = request.GET.get('q', '')
    selected_format = request.GET.get('format', '')

    qualifications_list = Qualification.objects.all().order_by('name')
    if search_query:
        qualifications_list = qualifications_list.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    if selected_format:
        qualifications_list = qualifications_list.filter(format=selected_format)
    
    paginator = Paginator(qualifications_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'format_choices': Qualification.FORMAT_CHOICES,
        'selected_format': selected_format,
    }
    return render(request, 'programs_view.html', context)

def program_detail(request, pk):
    qualification = get_object_or_404(Qualification, pk=pk)

    modules_by_year = qualification.get_modules_by_year_and_semester()

    core_modules_count = qualification.qualificationmodule_set.filter(module_type='Core').count()
    auxiliary_modules_count = qualification.qualificationmodule_set.filter(module_type='Auxiliary').count()

    context = {
        'qualification': qualification,
        'modules_by_year': modules_by_year,
        'core_modules_count': core_modules_count,
        'auxiliary_modules_count': auxiliary_modules_count,
    }
    return render(request, 'program_detail.html', context)

def modules_view(request):
    search_query = request.GET.get('q', '')
    selected_year = request.GET.get('year', '')
    selected_semester = request.GET.get('semester', '')

    modules_list = Module.objects.all().order_by('name')
    if search_query:
        modules_list = modules_list.filter(
            Q(name__icontains=search_query) |
            Q(code__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    if selected_year:
        modules_list = modules_list.filter(year=selected_year)
    if selected_semester:
        modules_list = modules_list.filter(semester=selected_semester)

    paginator = Paginator(modules_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    year_choices = Module.objects.values_list('year', flat=True).distinct().order_by('year')

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'year_choices': year_choices,
        'semester_choices': Module.SEMESTER_CHOICES,
        'selected_year': int(selected_year) if selected_year else '',
        'selected_semester': int(selected_semester) if selected_semester else '',
    }
    return render(request, 'modules_view.html', context)

def module_detail(request, pk):
    module = get_object_or_404(Module.objects.prefetch_related('learning_outcomes'), pk=pk)
    return render(request, 'module_detail.html', {'module': module})

def lecturers_view(request):
    search_query = request.GET.get('q', '')
    selected_type = request.GET.get('type', '')
    selected_qual = request.GET.get('qual', '')

    lecturers_list = Lecturer.objects.annotate(module_count=Count('module')).order_by('last_name', 'first_name')
    if search_query:
        lecturers_list = lecturers_list.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(expertise_areas__icontains=search_query)
        )
    if selected_type:
        lecturers_list = lecturers_list.filter(lecturer_type=selected_type)
    if selected_qual:
        lecturers_list = lecturers_list.filter(highest_qualification=selected_qual)

    paginator = Paginator(lecturers_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'type_choices': Lecturer.LECTURER_TYPE_CHOICES,
        'qual_choices': Lecturer.QUALIFICATION_CHOICES,
        'selected_type': selected_type,
        'selected_qual': selected_qual,
    }
    return render(request, 'lecturers_view.html', context)

def lecturer_detail(request, pk):
    lecturer = get_object_or_404(Lecturer, pk=pk)
    return render(request, 'lecturer_detail.html', {'lecturer': lecturer})

def resources_view(request):
    rules = AcademicRule.objects.all()
    return render(request, 'resources_view.html', {'rules': rules})
