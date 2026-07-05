from rest_framework import serializers
from .models import Job, User, Candidate, Employer, Application


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['employer']

    def validate(self, data):
        salary_min = data.get('salary_min')
        salary_max = data.get('salary_max')

        if (
            salary_min is not None
            and salary_max is not None
            and salary_max < salary_min
        ):
            raise serializers.ValidationError(
                "Maximum salary cannot be less than minimum salary."
            )

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CandidateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = [
            'id',
            'user',
            'skills',
            'education',
            'experience',
            'expected_salary',
            'resume',
            'is_deleted'
        ]

        read_only_fields = ['user', 'is_deleted']

    def validate_experience(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Experience cannot be negative."
            )
        return value

    def validate_expected_salary(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Expected salary cannot be negative."
            )
        return value
    def validate_resume(self, value):
        allowed_extensions = ['pdf', 'doc', 'docx']
        extension = value.name.split('.')[-1].lower()

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                "Only PDF, DOC, and DOCX files are allowed."
            )

        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(
                "Resume file size cannot exceed 5 MB."
            )

        return value


class EmployerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employer
        fields = [
            'id',
            'user',
            'company_name',
            'domain',
            'company_size',
            'is_verified',
            'is_deleted'
        ]

        read_only_fields = [
            'user',
            'is_verified',
            'is_deleted'
        ]

    def validate_company_size(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Company size cannot be negative."
            )
        return value
class ApplicationSerializer(serializers.ModelSerializer):

    job_title = serializers.CharField(
        source='job.title',
        read_only=True
    )

    class Meta:
        model = Application
        fields = [
            'id',
            'candidate',
            'job',
            'job_title',
            'resume_snapshot',
            'status',
            'applied_at',
            'updated_at'
        ]

        read_only_fields = [
            'candidate',
            'resume_snapshot',
            'status',
            'applied_at',
            'updated_at'
        ]