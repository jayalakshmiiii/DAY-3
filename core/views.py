from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.hashers import check_password
from django.db.models import Q

from .models import Job, User, Candidate, Employer
from .serializers import (
    JobSerializer,
    UserSerializer,
    CandidateProfileSerializer,
    EmployerProfileSerializer
)
from .auth_serializers import SignupSerializer
from .permissions import (
    IsAdmin,
    IsEmployer,
    IsCandidate
)
class HomeAPI(APIView):

    def get(self, request):
        return Response({
            "message": "Welcome to Zecpath Backend"
        })
class JobListAPI(APIView):

    def get(self, request):
        jobs = Job.objects.select_related(
            'employer',
            'employer__user'
        ).filter(
            status='active'
        ).order_by('-created_at')

        search = request.query_params.get('search')
        skill = request.query_params.get('skill')
        location = request.query_params.get('location')
        job_type = request.query_params.get('job_type')
        experience_min = request.query_params.get('experience_min')
        experience_max = request.query_params.get('experience_max')
        salary_min = request.query_params.get('salary_min')
        salary_max = request.query_params.get('salary_max')
        featured = request.query_params.get('featured')

        if search:
            jobs = jobs.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(skills__icontains=search)
            )

        if skill:
            jobs = jobs.filter(skills__icontains=skill)

        if location:
            jobs = jobs.filter(location__icontains=location)

        if job_type:
            jobs = jobs.filter(job_type=job_type)

        if experience_min:
            jobs = jobs.filter(experience__gte=experience_min)

        if experience_max:
            jobs = jobs.filter(experience__lte=experience_max)

        if salary_min:
            jobs = jobs.filter(salary_max__gte=salary_min)

        if salary_max:
            jobs = jobs.filter(salary_min__lte=salary_max)

        if featured == 'true':
            jobs = jobs.filter(is_featured=True)

        paginator = PageNumberPagination()
        paginator.page_size = 5

        paginated_jobs = paginator.paginate_queryset(
            jobs,
            request
        )

        serializer = JobSerializer(
            paginated_jobs,
            many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )


class JobCreateAPI(APIView):

    permission_classes = [IsEmployer]

    def post(self, request):
        employer = Employer.objects.get(
            user=request.user,
            is_deleted=False
        )

        serializer = JobSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save(employer=employer)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class EmployerJobManageAPI(APIView):

    permission_classes = [IsEmployer]

    def put(self, request, job_id):
        employer = Employer.objects.get(
            user=request.user,
            is_deleted=False
        )

        try:
            job = Job.objects.get(
                id=job_id,
                employer=employer
            )
        except Job.DoesNotExist:
            return Response(
                {"error": "Job not found or access denied"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = JobSerializer(
            job,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class ApplyJobAPI(APIView):

    permission_classes = [IsCandidate]

    def post(self, request):

        return Response({
            "message": "Job application submitted"
        })
class AdminDashboardAPI(APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        return Response({
            "message": "Welcome Admin"
        })

class UserTestAPI(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
class SignupAPI(APIView):

    def post(self, request):

        serializer = SignupSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "User created"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginAPI(APIView):

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)

            if not check_password(password, user.password):
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })

        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

class ProtectedAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({
            "message": "JWT works"
        })
class CandidateProfileAPI(APIView):

    permission_classes = [IsCandidate]

    def get(self, request):
        profile = Candidate.objects.get(
            user__email=request.user.email,
            is_deleted=False
        )

        serializer = CandidateProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = Candidate.objects.get(
            user__email=request.user.email,
            is_deleted=False
        )

        serializer = CandidateProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request):
        profile = Candidate.objects.get(
            user__email=request.user.email
        )

        profile.is_deleted = True
        profile.save()

        return Response({
            "message": "Candidate profile deleted"
        })


class EmployerProfileAPI(APIView):

    permission_classes = [IsEmployer]

    def get(self, request):
        profile = Employer.objects.get(
            user__email=request.user.email,
            is_deleted=False
        )

        serializer = EmployerProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = Employer.objects.get(
            user__email=request.user.email,
            is_deleted=False
        )

        serializer = EmployerProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request):
        profile = Employer.objects.get(
            user__email=request.user.email
        )

        profile.is_deleted = True
        profile.save()

        return Response({
            "message": "Employer profile deleted"
        })