from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

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
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


class JobCreateAPI(APIView):

    permission_classes = [IsEmployer]

    def post(self, request):

        serializer = JobSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

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

            user = User.objects.get(
                email=email,
                password=password
            )

            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })

        except User.DoesNotExist:

            return Response(
                {
                    "error": "Invalid credentials"
                },
                status=400
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