from django.db import models
import os
import uuid

class User(models.Model):

    ADMIN = "admin"
    EMPLOYER = "employer"
    CANDIDATE = "candidate"

    ROLE_CHOICES = (
        (ADMIN, "Admin"),
        (EMPLOYER, "Employer"),
        (CANDIDATE, "Candidate"),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def is_authenticated(self):
        return True
    def __str__(self):
        return self.email


class Employer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    company_name = models.CharField(max_length=200)
    domain = models.CharField(max_length=200)
    company_size = models.PositiveIntegerField()
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name

def resume_upload_path(instance, filename):
    extension = os.path.splitext(filename)[1].lower()
    new_filename = f"{uuid.uuid4().hex}{extension}"
    return os.path.join("resumes", new_filename)
class Candidate(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    skills = models.TextField()
    education = models.CharField(max_length=200)
    experience = models.PositiveIntegerField(default=0)
    expected_salary = models.PositiveIntegerField()
    is_deleted = models.BooleanField(default=False)
    resume = models.FileField(
    upload_to=resume_upload_path,
    null=True,
    blank=True
)

    def __str__(self):
        return self.user.name

class Job(models.Model):
    employer = models.ForeignKey(
        Employer,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.IntegerField()

    def __str__(self):
        return self.title


class Application(models.Model):
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    status = models.CharField(max_length=50)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate} - {self.job}"