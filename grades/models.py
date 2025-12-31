from django.db import models
from django.contrib.auth.models import User

class Semester(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()
    academic_year = models.CharField(max_length=9)

    class Meta:
        unique_together = ('user', 'number', 'academic_year')
        ordering = ['number']

    def __str__(self):
        return f"Семестр {self.number} ({self.academic_year})"

class Discipline(models.Model):
    DISCIPLINE_TYPES = [
        ('lecture', 'Лекционный курс'),
        ('practice', 'Практика'),
        ('coursework', 'Курсовая работа'),
        ('project', 'Проект'),
        ('exam', 'Экзамен'),
        ('other', 'Другое'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='disciplines')
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=DISCIPLINE_TYPES, default='lecture')
    expected_grade = models.CharField(max_length=10, blank=True, choices=[
        ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')
    ])
    actual_grade = models.CharField(max_length=10, blank=True, choices=[
        ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')
    ])
    for_diploma = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"

    @staticmethod
    def calculate_gpa(disciplines):
        grade_map = {
            "5": 5, "4": 4, "3": 3, "2": 2,
            "отлично": 5, "хорошо": 4, "удовл": 3, "неуд": 2,
            "A": 5, "B": 4, "C": 3, "D": 2, "F": 1
        }
        total, count = 0, 0
        for d in disciplines:
            if d.actual_grade and d.actual_grade in grade_map:
                total += grade_map[d.actual_grade]
                count += 1
        return round(total / count, 2) if count else 0

    @staticmethod
    def calculate_diploma_gpa(user):
        disciplines = Discipline.objects.filter(user=user, for_diploma=True)
        return Discipline.calculate_gpa(disciplines)