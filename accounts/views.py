from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import  redirect, render, get_object_or_404

from .models import AcademicGroup, Course, Department, StudentProfile
from .forms import DepartmentForm, AcademicGroupForm, CourseForm

from django.contrib.auth.decorators import login_required

from django.db.models import Count, Q

import csv
from django.http import HttpResponse


def is_methodist(user):
    return user.groups.filter(
        name='Методист'
    ).exists()

@login_required
def profile(request):
    return render(
        request,
        'profile.html',
        {
            'is_methodist': is_methodist(
                request.user
            )
        }
    )

@login_required
def course_list(request):
    courses = Course.objects.select_related('department').all()
    return render(
        request,
        'course_list.html',
        {
            'courses': courses,
        }
    )

# Работа с факультетами

@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(
        request,
        'department_list.html',
        {
            'departments': departments,
            'is_methodist': is_methodist(request.user),
        }
    )

@login_required
@user_passes_test(is_methodist)
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(
            request.POST
        )

        if form.is_valid():
            form.save()
            return redirect(
                'department_list'
            )
    else:
        form = DepartmentForm()
    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Добавление факультета',
        }
    )

@login_required
@user_passes_test(is_methodist)
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(
            request.POST, instance=department
        )
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(
        request, 'object_form.html',
        {
            'form': form,
            'title': 'Изменение факультета',
        }
    )

@login_required
@user_passes_test(is_methodist)
def department_delete(
        request,
        pk
):
    department = get_object_or_404(
        Department,
        pk=pk
    )
    if request.method == 'POST':

        department.delete()

        return redirect(
            'department_list'
        )
    return render(
        request,
        'object_confirm_delete.html',
        {
            'object': department,
            'title': 'Удаление факультета',
        }
    )

# Работа с учебными группами

@login_required
def academic_group_list(request):
    groups = AcademicGroup.objects.select_related('department').all()
    return render(
        request,
        'academic_group_list.html',
        {
            'groups': groups,
            'is_methodist': is_methodist(request.user),
        }
    )

@login_required
@user_passes_test(is_methodist)
def academic_group_create(request):
    if request.method == 'POST':
        form = AcademicGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('academic_group_list')
    else:
        form = AcademicGroupForm()
    return render(
        request, 'object_form.html',
        {'form': form, 'title': 'Добавление учебной группы'}
    )

@login_required
@user_passes_test(is_methodist)
def academic_group_update(request, pk):
    group = get_object_or_404(AcademicGroup, pk=pk)
    if request.method == 'POST':
        form = AcademicGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('academic_group_list')
    else:
        form = AcademicGroupForm(instance=group)
    return render(
        request, 'object_form.html',
        {'form': form, 'title': 'Изменение учебной группы'}
    )

@login_required
@user_passes_test(is_methodist)
def academic_group_delete(request, pk):
    group = get_object_or_404(AcademicGroup, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('academic_group_list')
    return render(
        request, 'object_confirm_delete.html',
        {'object': group, 'title': 'Удаление учебной группы'}
    )

# Работа с курсами

@login_required
def course_list(request):
    courses = Course.objects.select_related('department').all()
    return render(
        request,
        'course_list.html',
        {
            'courses': courses,
            'is_methodist': is_methodist(request.user),  # Добавлено для показа кнопок
        }
    )

@login_required
@user_passes_test(is_methodist)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(
        request, 'object_form.html',
        {'form': form, 'title': 'Добавление курса'}
    )

@login_required
@user_passes_test(is_methodist)
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(
        request, 'object_form.html',
        {'form': form, 'title': 'Изменение курса'}
    )

@login_required
@user_passes_test(is_methodist)
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(
        request, 'object_confirm_delete.html',
        {'object': course, 'title': 'Удаление курса'}
    )


#Учебные группы

@login_required
def academic_group_list(request):
    groups = AcademicGroup.objects.select_related('department').all()
    return render(request, 'academic_group_list.html', {
        'groups': groups,
        'is_methodist': is_methodist(request.user),
    })

@login_required
@user_passes_test(is_methodist)
def academic_group_create(request):
    if request.method == 'POST':
        form = AcademicGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('academic_group_list')
    else:
        form = AcademicGroupForm()
    return render(request, 'object_form.html', {'form': form, 'title': 'Добавление группы'})

@login_required
@user_passes_test(is_methodist)
def academic_group_update(request, pk):
    group = get_object_or_404(AcademicGroup, pk=pk)
    if request.method == 'POST':
        form = AcademicGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('academic_group_list')
    else:
        form = AcademicGroupForm(instance=group)
    return render(request, 'object_form.html', {'form': form, 'title': 'Изменение группы'})

@login_required
@user_passes_test(is_methodist)
def academic_group_delete(request, pk):
    group = get_object_or_404(AcademicGroup, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('academic_group_list')
    return render(request, 'object_confirm_delete.html', {'object': group, 'title': 'Удаление группы'})


#курсы

@login_required
def course_list(request):
    courses = Course.objects.select_related('department').all()
    return render(request, 'course_list.html', {
        'courses': courses,
        'is_methodist': is_methodist(request.user),
    })

@login_required
@user_passes_test(is_methodist)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'object_form.html', {'form': form, 'title': 'Добавление курса'})

@login_required
@user_passes_test(is_methodist)
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'object_form.html', {'form': form, 'title': 'Изменение курса'})

@login_required
@user_passes_test(is_methodist)
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'object_confirm_delete.html', {'object': course, 'title': 'Удаление курса'})


# accounts/views.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.shortcuts import render
from .models import StudentProfile, Course, Department, Violation

@login_required
@user_passes_test(is_methodist)
def dashboard_view(request):
    total_students = StudentProfile.objects.count()
    total_groups = AcademicGroup.objects.count() if 'AcademicGroup' in globals() else 0

    dept_stats = StudentProfile.objects.values('department__name').annotate(count=Count('id'))
    dept_labels = [item['department__name'] or 'Не указан' for item in dept_stats]
    dept_data = [item['count'] for item in dept_stats]

    course_popularity = Course.objects.annotate(
        student_count=Count('students')
    ).order_by('-student_count')[:8]
    pop_labels = [c.title for c in course_popularity]
    pop_data = [c.student_count for c in course_popularity]

    rel_stats = StudentProfile.objects.values('relationship_status').annotate(count=Count('id'))
    rel_map = {item['relationship_status']: item['count'] for item in rel_stats}
    singles_count = rel_map.get('single', 0)
    couples_count = rel_map.get('couple', 0)

    top_violators = StudentProfile.objects.annotate(
        violation_count=Count('violations')
    ).filter(
        violation_count__gt=0
    ).order_by('-violation_count')[:5]

    violator_names = [vp.user.username for vp in top_violators]
    violator_counts = [vp.violation_count for vp in top_violators]

    context = {
        'total_students': total_students,
        'total_groups': total_groups,

        'dept_labels': dept_labels,
        'dept_data': dept_data,

        'pop_labels': pop_labels,
        'pop_data': pop_data,

        'singles_count': singles_count,
        'couples_count': couples_count,

        'top_violator_names': violator_names,
        'top_violator_counts': violator_counts,
    }

    return render(request, 'dashboard.html', context)


# accounts/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import CourseProposal, Curriculum, CurriculumCourseLink, ProposalEventLog
from .serializers import (CourseProposalSerializer, CurriculumSerializer,
                          ProposalEventLogSerializer, ProposalStatusSerializer)


class CourseProposalViewSet(viewsets.ModelViewSet):
    serializer_class = CourseProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Методисты видят все, остальные - только свои
        if user.groups.filter(name='Методист').exists():
            return CourseProposal.objects.all().select_related('author', 'reviewer')
        return CourseProposal.objects.filter(author=user).select_related('author', 'reviewer')

    def perform_create(self, serializer):
        proposal = serializer.save(author=self.request.user)
        ProposalEventLog.objects.create(
            proposal=proposal,
            action='CREATED',
            details='Предложение курса создано',
            performed_by=self.request.user
        )

    @action(detail=True, methods=['patch'], url_path='change-status')
    def change_status(self, request, pk=None):

        proposal = self.get_object()
        serializer = ProposalStatusSerializer(
            data=request.data,
            context={'proposal': proposal, 'request': request}
        )
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data['new_status']
        comment = serializer.validated_data.get('comment', '')

        try:
            with transaction.atomic():  # ТРЕБОВАНИЕ П.6: ТРАНЗАКЦИЯ
                old_status = proposal.status
                proposal.status = new_status
                proposal.reviewer = request.user
                proposal.save()

                # СОСТАВНАЯ ОПЕРАЦИЯ: При одобрении добавляем в активный учебный план
                if new_status == 'approved':
                    active_plan = Curriculum.objects.filter(is_active=True).first()
                    if not active_plan:
                        raise ValueError("Нет активного учебного плана для добавления курса")

                    # Проверяем, не добавлен ли уже
                    link, created = CurriculumCourseLink.objects.get_or_create(
                        curriculum=active_plan,
                        proposal=proposal
                    )
                    if created:
                        # Обновляем общую нагрузку плана
                        active_plan.total_credits += proposal.credits
                        active_plan.save()

                        ProposalEventLog.objects.create(
                            proposal=proposal,
                            action='ADDED_TO_PLAN',
                            details=f'Добавлен в план "{active_plan.name}" (+{proposal.credits} ЗЕ)',
                            performed_by=request.user
                        )

                # Логируем изменение статуса
                ProposalEventLog.objects.create(
                    proposal=proposal,
                    action=f'STATUS_CHANGED: {old_status} -> {new_status}',
                    details=comment or f'Статус изменен с "{proposal.get_status_display()}"',
                    performed_by=request.user
                )

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(CourseProposalSerializer(proposal).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        qs = self.get_queryset()
        return Response({
            'total': qs.count(),
            'draft': qs.filter(status='draft').count(),
            'submitted': qs.filter(status='submitted').count(),
            'approved': qs.filter(status='approved').count(),
            'rejected': qs.filter(status='rejected').count(),
        })


class CurriculumViewSet(viewsets.ModelViewSet):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer
    permission_classes = [permissions.IsAdminUser]  # Только админы управляют планами


class ProposalEventLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProposalEventLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        proposal_id = self.kwargs.get('proposal_pk')
        if proposal_id:
            return ProposalEventLog.objects.filter(proposal_id=proposal_id)

        user = self.request.user
        if user.groups.filter(name='Методист').exists():
            return ProposalEventLog.objects.all()
        return ProposalEventLog.objects.filter(proposal__author=user)


@login_required
def course_approval_view(request):
    return render(request, 'accounts/course_approval.html')

@action(detail=False, methods=['get'])
def export_csv(self, request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="proposals.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Название', 'Автор', 'Статус', 'ЗЕ', 'Дата'])

    for obj in self.get_queryset():
        writer.writerow([obj.id, obj.title, obj.author.username, obj.get_status_display(), obj.credits,
                         obj.created_at.strftime('%d.%m.%Y')])

    return response