from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


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

class CourseProposal(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('submitted', 'На согласовании'),
        ('approved', 'Согласован'),
        ('rejected', 'Отклонен'),
    ]

    title = models.CharField(max_length=200, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание и цели")
    credits = models.PositiveIntegerField(default=3, verbose_name="Количество зачетных единиц")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Статус")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_proposals',
                               verbose_name="Автор")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='reviewed_proposals', verbose_name="Проверивший методист")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Предложение курса"
        verbose_name_plural = "Предложения курсов"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} [{self.get_status_display()}]"


class Curriculum(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название плана")
    academic_year = models.CharField(max_length=9, verbose_name="Учебный год")
    total_credits = models.PositiveIntegerField(default=0, verbose_name="Общее количество ЗЕ")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Учебный план"
        verbose_name_plural = "Учебные планы"

    def __str__(self):
        return f"{self.name} ({self.academic_year})"


class CurriculumCourseLink(models.Model):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='courses')
    proposal = models.ForeignKey(CourseProposal, on_delete=models.CASCADE, related_name='curriculum_links')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Курс в учебном плане"
        verbose_name_plural = "Курсы в учебных планах"
        unique_together = ['curriculum', 'proposal']


class ProposalEventLog(models.Model):
    ACTION_CHOICES = [
        ('CREATED', 'Создано'),
        ('SUBMITTED', 'Отправлено на согласование'),
        ('APPROVED', 'Согласовано'),
        ('REJECTED', 'Отклонено'),
        ('ADDED_TO_PLAN', 'Добавлено в учебный план'),
    ]

    proposal = models.ForeignKey(CourseProposal, on_delete=models.CASCADE, related_name='events')
    action = models.CharField(max_length=100, choices=ACTION_CHOICES, verbose_name="Действие") # УВЕЛИЧЕНО до 100
    details = models.TextField(blank=True, verbose_name="Подробности")
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                     verbose_name="Инициатор")
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Событие предложения"
        verbose_name_plural = "История событий"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.proposal.title} - {self.get_action_display()} ({self.timestamp})"