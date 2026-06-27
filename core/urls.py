from django.urls import path

from .views import (
    AdminDashboardAPI,
    ApplyJobAPI,
    JobListAPI,
    JobCreateAPI,
    UserTestAPI,
    ProtectedAPI
)

urlpatterns = [
    path('jobs/', JobListAPI.as_view()),
    path('jobs/create/', JobCreateAPI.as_view()),
    path('users/', UserTestAPI.as_view()),
    path('protected/', ProtectedAPI.as_view()),
    path('apply/',ApplyJobAPI.as_view()
),

path('admin-dashboard/',AdminDashboardAPI.as_view()),
]