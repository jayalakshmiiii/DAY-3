from django.urls import path

from .views import (
    AdminDashboardAPI,
    ApplyJobAPI,
    EmployerJobManageAPI,
    JobListAPI,
    JobCreateAPI,
    UserTestAPI,
    ProtectedAPI,
    CandidateProfileAPI,
    EmployerProfileAPI,

)

urlpatterns = [
    path('jobs/', JobListAPI.as_view()),
    path('jobs/create/', JobCreateAPI.as_view()),
    path('users/', UserTestAPI.as_view()),
    path('protected/', ProtectedAPI.as_view()),
    path('apply/', ApplyJobAPI.as_view()),
    path('admin-dashboard/', AdminDashboardAPI.as_view()),
    path('profile/candidate/', CandidateProfileAPI.as_view()),
    path('profile/employer/', EmployerProfileAPI.as_view()),
    path('jobs/<int:job_id>/manage/',EmployerJobManageAPI.as_view()),
]