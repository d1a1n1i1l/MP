from django.urls import path
from . import views

app_name = 'grades'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('semester/<int:semester_id>/', views.semester_detail, name='semester_detail'),
    path('semester/add/', views.add_semester, name='add_semester'),
    path('semester/<int:semester_id>/add/', views.add_discipline, name='add_discipline'),
    path('discipline/<int:discipline_id>/delete/', views.delete_discipline, name='delete_discipline'),
    path('diploma/', views.diploma_view, name='diploma'),
    path('diploma/export/', views.export_diploma_excel, name='export_diploma_excel'),
    path('semester/<int:semester_id>/export/', views.export_transcript_excel, name='export_transcript_excel'),
]