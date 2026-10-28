from rest_framework import serializers
from .models import CourseProposal, Curriculum, CurriculumCourseLink, ProposalEventLog


class ProposalStatusSerializer(serializers.Serializer):
    """СерIALIZATOR ДЛЯ СМЕНЫ СТАТУСА С ВАЛИДАЦИЕЙ"""
    new_status = serializers.ChoiceField(choices=CourseProposal.STATUS_CHOICES)
    comment = serializers.CharField(required=False, allow_blank=True)

    def validate_new_status(self, value):
        proposal = self.context['proposal']

        # Бизнес-правило 1: Нельзя изменить статус согласованного курса
        if proposal.status == 'approved' and value != 'approved':
            raise serializers.ValidationError("Нельзя изменить статус согласованного курса.")

        # Бизнес-правило 2: Нельзя одобрить черновик напрямую
        if value == 'approved' and proposal.status == 'draft':
            raise serializers.ValidationError("Сначала отправьте предложение на согласование.")

        # Бизнес-правило 3: Только методист может одобрять/отклонять
        user = self.context['request'].user
        if value in ['approved', 'rejected'] and not user.groups.filter(name='Методист').exists():
            raise serializers.ValidationError("Только методист может изменять этот статус.")

        return value


class CourseProposalSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    reviewer_username = serializers.ReadOnlyField(source='reviewer.username')
    status_display = serializers.ReadOnlyField(source='get_status_display')

    class Meta:
        model = CourseProposal
        fields = ['id', 'title', 'description', 'credits', 'status', 'status_display',
                  'author', 'author_username', 'reviewer', 'reviewer_username',
                  'created_at', 'updated_at']
        read_only_fields = ['author', 'reviewer', 'created_at', 'updated_at']


class CurriculumSerializer(serializers.ModelSerializer):
    course_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Curriculum
        fields = '__all__'


class ProposalEventLogSerializer(serializers.ModelSerializer):
    performed_by_username = serializers.ReadOnlyField(source='performed_by.username')
    action_display = serializers.ReadOnlyField(source='get_action_display')

    class Meta:
        model = ProposalEventLog
        fields = ['id', 'action', 'action_display', 'details', 'performed_by',
                  'performed_by_username', 'timestamp']