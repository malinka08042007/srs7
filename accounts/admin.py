from django.contrib import admin
from .models import (
 AcademicGroup,
 Course,
 Department,
 StudentProfile,
Violation,
)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'department')
    list_filter = ('department',)
    search_fields = ('title',)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'department')
    list_filter = ('department',)
    search_fields = ('user__username',)
    filter_horizontal = ('courses',)


@admin.register(AcademicGroup)
class AcademicGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department')
    list_filter = ('department',)
    search_fields = ('name',)

@admin.register(Violation)
class ViolationAdmin(admin.ModelAdmin):
    list_display = ('student', 'violation_type', 'date')
    list_filter = ('violation_type', 'date')
from .models import CourseProposal, Curriculum, ProposalEventLog

@admin.register(CourseProposal)
class CourseProposalAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'author', 'created_at')
    list_filter = ('status',)

@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year', 'total_credits', 'is_active')

@admin.register(ProposalEventLog)
class ProposalEventLogAdmin(admin.ModelAdmin):
    list_display = ('proposal', 'action', 'performed_by', 'timestamp')