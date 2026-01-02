from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Semester, Discipline
from django.http import HttpResponseRedirect

@login_required
def dashboard(request):
    semesters = Semester.objects.filter(user=request.user)
    
    # Только данные по семестрам
    semester_data = []
    for s in semesters:
        disciplines = s.disciplines.all()
        gpa = Discipline.calculate_gpa(disciplines)
        semester_data.append({
            'semester': s,
            'gpa': gpa,
            'discipline_count': disciplines.count()
        })
    
    return render(request, 'grades/dashboard.html', {
        'semester_data': semester_data
        # Убрано: 'diploma_gpa': ...
    })
        
        
@login_required
def semester_detail(request, semester_id):
    """Детали семестра: список дисциплин + GPA"""
    semester = get_object_or_404(Semester, id=semester_id, user=request.user)
    disciplines = semester.disciplines.all()
    gpa = Discipline.calculate_gpa(disciplines)
    return render(request, 'grades/semester_detail.html', {
        'semester': semester,
        'disciplines': disciplines,
        'gpa': gpa
    })

@login_required
def add_semester(request):
    """Создать новый семестр"""
    if request.method == 'POST':
        Semester.objects.create(
            user=request.user,
            number=request.POST['number'],
            academic_year=request.POST['academic_year']
        )
        return redirect('grades:dashboard')
    return render(request, 'grades/add_semester.html')

@login_required
def add_discipline(request, semester_id):
    """Добавить дисциплину в семестр"""
    semester = get_object_or_404(Semester, id=semester_id, user=request.user)
    if request.method == 'POST':
        Discipline.objects.create(
            user=request.user,
            semester=semester,
            title=request.POST['title'],
            assessment_type=request.POST.get('assessment_type', 'exam'),
            expected_grade=request.POST.get('expected_grade', ''),
            actual_grade=request.POST.get('actual_grade', ''),
            for_diploma='for_diploma' in request.POST
        )
        return redirect('grades:semester_detail', semester_id=semester.id)
    return render(request, 'grades/add_discipline.html', {'semester': semester})
@login_required
def delete_discipline(request, discipline_id):
    discipline = get_object_or_404(Discipline, id=discipline_id, user=request.user)
    semester_id = discipline.semester.id
    discipline.delete()
    return redirect('grades:semester_detail', semester_id=semester_id)
@login_required
def diploma_view(request):
    """Страница диплома: только дисциплины с for_diploma=True"""
    disciplines = Discipline.objects.filter(user=request.user, for_diploma=True).select_related('semester')
    gpa = Discipline.calculate_gpa(disciplines)
    return render(request, 'grades/diploma.html', {
        'disciplines': disciplines,
        'gpa': gpa
    })  