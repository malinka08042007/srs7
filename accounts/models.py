from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='courses'
    )

    def __str__(self):
        return self.title


class AcademicGroup(models.Model):
    name = models.CharField(max_length=50)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='groups'
    )

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )
    academic_group = models.ForeignKey(
        AcademicGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )
    courses = models.ManyToManyField(
        Course,
        blank=True,
        related_name='students'
    )

    RELATIONSHIP_CHOICES = [
        ('single', 'Холостяк/Холостячка'),
        ('couple', 'Состоит в паре'),
    ]
    relationship_status = models.CharField(
        max_length=10,
        choices=RELATIONSHIP_CHOICES,
        default='single'
    )
    def __str__(self):
        return self.user.username


class Violation(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='violations'
    )
    description = models.TextField(max_length=200)
    date = models.DateField(auto_now_add=True)

    VIOLATION_TYPES = [
        ('magic', 'Магия вне уроков'),
        ('forbidden', 'Запретный лес'),
        ('disrespect', 'Неуважение к Инквизитору'),
        ('other', 'Прочее'),
    ]
    violation_type = models.CharField(
        max_length=20,
        choices=VIOLATION_TYPES,
        default='other'
    )

    def __str__(self):
        return f"Нарушение: {self.student.user.username} ({self.date})"