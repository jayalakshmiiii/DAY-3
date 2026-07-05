# Zecpath Backend API Documentation

## Overview

Zecpath is a role-based recruitment platform backend built using Django REST Framework.

Supported roles:

- Admin
- Employer
- Candidate

Authentication is handled using JWT access and refresh tokens.

---

## Base URL

http://127.0.0.1:8000

---

## Authentication Flow

1. User creates an account using the Signup API.
2. The password is securely hashed before storage.
3. User logs in using email and password.
4. The server returns an access token and refresh token.
5. The access token is sent as a Bearer token for protected APIs.
6. Role-based permissions control access to Candidate, Employer, and Admin endpoints.

Flow:

Signup → Password Hashing → Login → JWT Token → Authentication → Role Permission → Protected API

---

## Authentication APIs

### Signup

Method: POST

Endpoint:

/api/auth/signup/

Example Request:

{
    "name": "Test Candidate",
    "email": "candidate@example.com",
    "phone": "9876543210",
    "role": "candidate",
    "password": "securepassword"
}

Success Status:

201 Created

---

### Login

Method: POST

Endpoint:

/api/auth/login/

Example Request:

{
    "email": "candidate@example.com",
    "password": "securepassword"
}

Success Response:

{
    "access": "access_token",
    "refresh": "refresh_token"
}

Success Status:

200 OK

---

## Authorization

Protected APIs require:

Authorization: Bearer <access_token>

Access token lifetime: 15 minutes

Refresh token lifetime: 7 days

---

## Job APIs

### List Jobs

Method: GET

Endpoint:

/api/jobs/

Features:

- Pagination
- Page size of 5
- Search
- Location filtering
- Optimized database queries

---

### Search Jobs

Method: GET

Example:

/api/jobs/?search=Python

---

### Filter Jobs by Location

Method: GET

Example:

/api/jobs/?location=Kochi

---

### Create Job

Method: POST

Endpoint:

/api/jobs/create/

Required Role:

Employer

---

### Apply for Job

Method: POST

Endpoint:

/api/apply/

Required Role:

Candidate

---

## Candidate Profile APIs

Endpoint:

/api/profile/candidate/

Supported Methods:

- GET - View profile
- PUT - Update profile
- DELETE - Soft delete profile

Required Role:

Candidate

Candidate profiles support secure resume uploads.

Allowed file types:

- PDF
- DOC
- DOCX

Maximum file size:

5 MB

Uploaded files use unique UUID filenames to prevent duplicate-name conflicts.

---

## Employer Profile APIs

Endpoint:

/api/profile/employer/

Supported Methods:

- GET - View profile
- PUT - Update profile
- DELETE - Soft delete profile

Required Role:

Employer

---

## Admin API

### Admin Dashboard

Method: GET

Endpoint:

/api/admin-dashboard/

Required Role:

Admin

Unauthorized roles receive:

403 Forbidden

---

## Standard Error Response

All API errors use a centralized response structure:

{
    "success": false,
    "status_code": 401,
    "errors": {
        "detail": "Authentication credentials were not provided."
    }
}

---

## HTTP Status Codes

- 200 OK - Request successful
- 201 Created - Resource created
- 400 Bad Request - Invalid request data
- 401 Unauthorized - Authentication failed
- 403 Forbidden - Permission denied
- 404 Not Found - Resource not found
- 500 Internal Server Error - Unexpected server error

---

## Security Features

- Password hashing
- JWT authentication
- Access and refresh token expiry
- Role-based permissions
- Unauthorized access protection
- File extension validation
- File size restriction
- Unique resume filenames
- Centralized error handling

---

## Performance Features

- Page-based pagination
- Keyword search
- Location filtering
- select_related() query optimization
- Prevention of N+1 queries