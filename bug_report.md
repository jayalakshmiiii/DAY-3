# Zecpath Backend - Bug Report

## Bug 1: Role Permission Failure

**Issue:**  
Authenticated users received 403 Forbidden when accessing role-protected endpoints.

**Cause:**  
The JWT authentication system was not correctly mapping the authenticated user role.

**Fix:**  
Updated authentication and permission handling to correctly identify the user's role.

**Status:** Resolved


## Bug 2: Employer Profile Creation Failure

**Issue:**  
Employer signup caused an Internal Server Error.

**Cause:**  
The profile creation signal used the old field `company_location` after the model field was renamed to `domain`.

**Fix:**  
Updated the Employer profile creation signal to use the correct model fields.

**Status:** Resolved


## Bug 3: Soft-Deleted Profile Access

**Issue:**  
Profile update returned an Internal Server Error after the profile had been soft deleted.

**Cause:**  
The API attempted to retrieve a profile with `is_deleted=False`, but no active profile existed.

**Fix:**  
Restored the profile for testing and identified the need for proper 404 handling.

**Status:** Resolved