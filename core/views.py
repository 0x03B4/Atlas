from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Qualification, Module, Lecturer, Student, AcademicRule
from .forms import StudentProfileForm

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

def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student_dashboard') 
        else:
            return render(request, 'student_login.html', {'error_message': 'Invalid username or password.'})
    return render(request, 'student_login.html')

def student_logout(request):
    """Logs the student out and redirects to the login page."""
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('student_login')

def student_signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'This email is already registered.')
            return render(request, 'student_signup.html')

        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            Student.objects.create(user=user) # Create a student profile for the new user

            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('student_login') # Redirect to login page after successful signup
        except Exception as e:
            messages.error(request, f'Error creating account: {e}')
            return render(request, 'student_signup.html')
    return render(request, 'student_signup.html')

@login_required
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)
    dashboard_context = student.get_dashboard_context()

    if not dashboard_context:
        messages.info(request, "Please complete your profile, including qualification, current year, and semester, to view the dashboard.")
        return redirect('student_profile')

    return render(request, 'student_dashboard.html', dashboard_context)

@login_required
def student_modules(request):
    student = get_object_or_404(Student, user=request.user)
    if not all([student.qualification, student.current_year, student.current_semester]):
        messages.info(request, "Please complete your profile, including qualification, current year, and semester, to view your modules.")
        return redirect('student_profile')
        
    qualification = student.qualification

    current_semester_modules = Module.objects.filter(
        year=student.current_year,
        semester=student.current_semester,
        qualificationmodule__qualification=qualification
    )

    context = {
        'current_semester_modules': current_semester_modules,
    }
    return render(request, 'student_modules.html', context)

@login_required
def student_qualification(request):
    student = get_object_or_404(Student, user=request.user)
    if student.qualification is None:
        messages.info(request, "Please select a qualification on your profile to view its details.")
        return redirect('student_profile')
        
    qualification = student.qualification
    modules_by_year = qualification.get_modules_by_year_and_semester()

    core_modules_count = qualification.qualificationmodule_set.filter(module_type='Core').count()
    auxiliary_modules_count = qualification.qualificationmodule_set.filter(module_type='Auxiliary').count()

    context = {
        'qualification': qualification,
        'modules_by_year': modules_by_year,
        'core_modules_count': core_modules_count,
        'auxiliary_modules_count': auxiliary_modules_count,
    }
    return render(request, 'student_qualification.html', context)

@login_required
def student_profile(request):
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('student_profile')
    else:
        form = StudentProfileForm(instance=student, user=request.user)

    context = {
        'student': student,
        'form': form,
    }
    return render(request, 'student_profile.html', context)