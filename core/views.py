from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Qualification


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