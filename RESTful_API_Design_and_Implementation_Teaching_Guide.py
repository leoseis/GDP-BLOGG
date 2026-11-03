# ================================================================
# NIIT BACKEND DEVELOPMENT TEACHING GUIDE
# TOPIC 1: RESTful API DESIGN AND IMPLEMENTATION
# Format: Python (.py) teaching notes for VS Code
# ================================================================
#
# IMPORTANT:
# This file is a TEACHING GUIDE. It is designed to be opened in VS Code
# and read from top to bottom. The examples are written as comments so
# that running this guide will not cause errors.
#
# The actual Django code should be copied into the matching files in
# your Django project: settings.py, models.py, serializers.py, views.py,
# and urls.py.
#
# ------------------------------------------------
# 1. LESSON OBJECTIVES
# ------------------------------------------------
#
# By the end of this lesson, students should be able to:
# 1. Explain what an API is.
# 2. Explain REST and RESTful APIs in simple terms.
# 3. Identify common HTTP methods and status codes.
# 4. Design resource-based API endpoints.
# 5. Create a basic REST API using Django REST Framework (DRF).
# 6. Use a serializer to convert model data into JSON and validate input.
# 7. Test API endpoints using a browser, Postman, or curl.
#
# ------------------------------------------------
# 2. WHAT IS AN API?
# ------------------------------------------------
#
# API means Application Programming Interface.
#
# An API is a way for two software applications to communicate.
#
# EXAMPLE:
# Imagine a school portal with:
# - A React frontend that displays students.
# - A Django backend that stores student records in a database.
#
# React should not connect directly to the database. Instead:
#
# React frontend ---> sends HTTP request ---> Django API
# Django API -------> reads/writes data ----> Database
# Django API -------> sends JSON response --> React frontend
#
# A simple API response might look like this:
#
# {
#     "id": 1,
#     "name": "Ada Okafor",
#     "email": "ada@example.com"
# }
#
# JSON means JavaScript Object Notation. It is a common format for
# exchanging data between frontend and backend applications.
#
# CLASS QUESTION:
# Why should a React application normally communicate with Django through
# an API instead of connecting directly to the database?
#
# ------------------------------------------------
# 3. WHAT DOES REST MEAN?
# ------------------------------------------------
#
# REST stands for Representational State Transfer.
#
# REST is a set of architectural principles commonly used to design web APIs.
# A RESTful API usually:
# - Organizes data around resources, such as students, courses, or books.
# - Uses standard HTTP methods such as GET, POST, PUT, PATCH, and DELETE.
# - Uses clear URLs to identify resources.
# - Sends and receives representations of data, commonly JSON.
# - Uses HTTP status codes to describe the result of a request.
#
# A resource is a thing or collection of things that the API manages.
#
# Examples of resources:
# - students
# - courses
# - teachers
# - books
# - blog posts
#
# ------------------------------------------------
# 4. DESIGNING GOOD API ENDPOINTS
# ------------------------------------------------
#
# An endpoint is a URL through which a client accesses an API resource.
#
# Example base URL:
# http://127.0.0.1:8000/api/
#
# Recommended student endpoints:
#
# GET     /api/students/       List all students
# POST    /api/students/       Create a student
# GET     /api/students/1/     Retrieve student with ID 1
# PUT     /api/students/1/     Replace/update student 1
# PATCH   /api/students/1/     Partially update student 1
# DELETE  /api/students/1/     Delete student 1
#
# Notice:
# - Use nouns such as "students", not action names such as "getStudents".
# - Use plural resource names consistently.
# - Use a trailing slash consistently in this Django example.
# - Use the resource ID to identify one particular record.
#
# Less clear:
# /api/getAllStudents/
# /api/createNewStudent/
# /api/deleteStudent/1/
#
# Clearer:
# /api/students/
# /api/students/1/
#
# IMPORTANT:
# These are common REST conventions, not absolute laws. Consistency and
# clear documentation are important.
#
# ------------------------------------------------
# 5. HTTP METHODS
# ------------------------------------------------
#
# GET:
# Reads data. It should not create, update, or delete records.
#
# POST:
# Usually creates a new record in a collection.
#
# PUT:
# Usually replaces the full representation of an existing record.
# Required fields may need to be supplied.
#
# PATCH:
# Updates only the fields supplied in the request.
#
# DELETE:
# Removes a resource.
#
# QUICK EXAMPLE:
# GET    /api/students/     -> view the student list
# POST   /api/students/     -> add a student
# GET    /api/students/3/   -> view student 3
# PATCH  /api/students/3/   -> update selected fields for student 3
# DELETE /api/students/3/   -> delete student 3
#
# ------------------------------------------------
# 6. COMMON HTTP STATUS CODES
# ------------------------------------------------
#
# 200 OK:
# The request succeeded. Often used for successful GET, PUT, or PATCH.
#
# 201 Created:
# A new resource was successfully created.
#
# 204 No Content:
# The request succeeded and there is no response body. Often used for DELETE.
#
# 400 Bad Request:
# The submitted data is invalid or the request is malformed.
#
# 401 Unauthorized:
# Authentication is missing or invalid. In API usage, this usually means
# the client must authenticate.
#
# 403 Forbidden:
# The server understood the request but refuses to allow it.
#
# 404 Not Found:
# The requested resource does not exist.
#
# 405 Method Not Allowed:
# The endpoint does not support the HTTP method used.
#
# 500 Internal Server Error:
# An unexpected server-side error occurred.
#
# CLASS ACTIVITY:
# Ask students which status code they expect when:
# 1. A student is created successfully.
# 2. A requested student ID does not exist.
# 3. An email field fails validation.
#
# Answers: 201, 404, and commonly 400.
#
# ------------------------------------------------
# 7. PRACTICAL PROJECT: BUILD A STUDENT REST API
# ------------------------------------------------
#
# We will build a small API that stores and returns student records.
#
# Assumptions:
# - Python is installed.
# - A virtual environment has already been created, if required by your class.
# - Students are working inside their Django project folder.
#
# STEP 1: INSTALL DJANGO AND DJANGO REST FRAMEWORK
# ------------------------------------------------
#
# Activate the project's virtual environment first.
#
# Linux/macOS example:
# source .venv/bin/activate
#
# Windows example:
# .venv\Scripts\activate
#
# Install the packages:
#
# pip install django djangorestframework
#
# If Django is already installed in the project's environment, pip will
# check the installed version and install any missing package.
#
# STEP 2: CREATE A DJANGO PROJECT (ONLY IF YOU DO NOT ALREADY HAVE ONE)
# --------------------------------------------------------------------
#
# django-admin startproject school_api
# cd school_api
# python manage.py startapp students
#
# If your class already has a Django project, do not create another project.
# Create only the app if it does not already exist.
#
# STEP 3: REGISTER THE APP AND DRF
# --------------------------------
#
# Open school_api/settings.py and add the following to INSTALLED_APPS:
#
# INSTALLED_APPS = [
#     # Keep the default Django apps here.
#     "rest_framework",
#     "students",
# ]
#
# Do not delete the existing Django apps. Add these entries to the list.
#
# ------------------------------------------------
# 8. CREATE THE STUDENT MODEL
# ------------------------------------------------
#
# Open students/models.py and add:
#
# from django.db import models
#
# class Student(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     department = models.CharField(max_length=100)
#     level = models.PositiveIntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.name
#
# EXPLANATION:
# - name stores the student's name.
# - email stores a valid email address and must be unique.
# - department stores the student's department.
# - level stores a positive integer, for example 100, 200, or 300.
# - created_at records when the student was created.
# - __str__ returns a readable name when the object is displayed.
#
# Create the database table:
#
# python manage.py makemigrations
# python manage.py migrate
#
# WHY DO WE MIGRATE?
# makemigrations creates migration instructions based on model changes.
# migrate applies those instructions to the database.
#
# ------------------------------------------------
# 9. CREATE A SERIALIZER
# ------------------------------------------------
#
# A serializer helps convert Django model objects into JSON-compatible data.
# It also validates incoming data before it is saved.
#
# Create a new file: students/serializers.py
#
# Add:
#
# from rest_framework import serializers
# from .models import Student
#
# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = [
#             "id",
#             "name",
#             "email",
#             "department",
#             "level",
#             "created_at",
#         ]
#         read_only_fields = ["id", "created_at"]
#
# EXPLANATION:
# - ModelSerializer connects the serializer to the Student model.
# - fields defines which fields the API can expose.
# - read_only_fields means the client cannot set these fields directly.
# - EmailField validation and the model's unique constraint help prevent
#   invalid or duplicate email addresses.
#
# IMPORTANT:
# A serializer does not replace a database model. The model defines the
# database structure; the serializer controls data conversion and validation.
#
# ------------------------------------------------
# 10. CREATE API VIEWS USING A MODEL VIEWSET
# ------------------------------------------------
#
# A ViewSet groups related API actions for a resource.
# ModelViewSet supplies common create, list, retrieve, update, partial update,
# and delete actions when configured with a queryset and serializer.
#
# Open students/views.py and add:
#
# from rest_framework import viewsets
# from .models import Student
# from .serializers import StudentSerializer
#
# class StudentViewSet(viewsets.ModelViewSet):
#     queryset = Student.objects.all().order_by("id")
#     serializer_class = StudentSerializer
#
# EXPLANATION:
# - queryset describes which Student records can be accessed.
# - order_by("id") makes the list order predictable for this exercise.
# - serializer_class tells DRF how to validate and represent student data.
# - ModelViewSet provides the standard CRUD actions.
#
# SECURITY NOTE:
# This example is for local classroom practice. It does not yet configure
# authentication or permissions. Do not expose a real student database
# publicly without appropriate permissions, authentication, validation,
# and privacy safeguards.
#
# ------------------------------------------------
# 11. CONNECT THE API URLS
# ------------------------------------------------
#
# Create students/urls.py:
#
# from rest_framework.routers import DefaultRouter
# from .views import StudentViewSet
#
# router = DefaultRouter()
# router.register("students", StudentViewSet, basename="student")
#
# urlpatterns = router.urls
#
# Now open the main project file school_api/urls.py and configure it:
#
# from django.contrib import admin
# from django.urls import path, include
#
# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("api/", include("students.urls")),
# ]
#
# The router automatically creates routes for the standard ViewSet actions.
# The main endpoints will include:
#
# /api/students/
# /api/students/<id>/
#
# ------------------------------------------------
# 12. RUN THE SERVER
# ------------------------------------------------
#
# In the terminal, run:
#
# python manage.py runserver
#
# Open this address in your browser:
#
# http://127.0.0.1:8000/api/students/
#
# DRF's browsable API may appear in the browser. It allows you to inspect
# responses and, depending on the request and permissions, submit requests.
#
# At first, the list should be empty because no students have been created.
#
# If you see an import error:
# - Check spelling of app and file names.
# - Confirm "students" and "rest_framework" are in INSTALLED_APPS.
# - Confirm serializers.py exists in the students folder.
# - Confirm migrations have been applied.
# - Read the full terminal traceback, starting from the final error message.
#
# ------------------------------------------------
# 13. TEST CREATE (POST)
# ------------------------------------------------
#
# Send a POST request to:
#
# http://127.0.0.1:8000/api/students/
#
# Example JSON body:
#
# {
#     "name": "Ada Okafor",
#     "email": "ada@example.com",
#     "department": "Computer Science",
#     "level": 200
# }
#
# In Postman:
# 1. Create a new HTTP request.
# 2. Select POST.
# 3. Enter the endpoint URL.
# 4. Select Body.
# 5. Select raw.
# 6. Choose JSON as the body type.
# 7. Paste the JSON above.
# 8. Click Send.
#
# Expected result:
# - Status: 201 Created.
# - Response: the newly created student, including the generated id.
#
# If you submit the same email again, validation should reject the duplicate.
# Depending on the request and serializer configuration, the response will
# commonly have status 400 Bad Request with an error message.
#
# ------------------------------------------------
# 14. TEST READ (GET)
# ------------------------------------------------
#
# A. List all students:
#
# GET http://127.0.0.1:8000/api/students/
#
# B. Retrieve one student:
#
# GET http://127.0.0.1:8000/api/students/1/
#
# Replace 1 with the actual ID returned when you created a student.
#
# Expected result:
# - A list of student objects for the collection endpoint.
# - One student object for the detail endpoint.
# - A missing ID normally returns 404 Not Found.
#
# ------------------------------------------------
# 15. TEST UPDATE (PUT AND PATCH)
# ------------------------------------------------
#
# PATCH is useful when changing only one or two fields.
#
# Example:
# PATCH http://127.0.0.1:8000/api/students/1/
#
# JSON body:
#
# {
#     "level": 300
# }
#
# Expected result: the student's level changes while the other fields remain.
#
# PUT generally represents a full update. For this example, supply all
# required writable fields:
#
# PUT http://127.0.0.1:8000/api/students/1/
#
# JSON body:
#
# {
#     "name": "Ada Okafor",
#     "email": "ada@example.com",
#     "department": "Software Engineering",
#     "level": 300
# }
#
# Use an existing student ID. A successful update commonly returns 200 OK.
#
# ------------------------------------------------
# 16. TEST DELETE
# ------------------------------------------------
#
# Send:
#
# DELETE http://127.0.0.1:8000/api/students/1/
#
# Expected result:
# - Commonly status 204 No Content.
# - The record is removed from the database.
# - A subsequent GET request for that ID should return 404.
#
# WARNING:
# DELETE is destructive. Use test records during practice, not real student
# records.
#
# ------------------------------------------------
# 17. TESTING WITH CURL (OPTIONAL)
# ------------------------------------------------
#
# GET the student list:
#
# curl http://127.0.0.1:8000/api/students/
#
# POST a student (run as one command in a terminal):
#
# curl -X POST http://127.0.0.1:8000/api/students/ \
#   -H "Content-Type: application/json" \
#   -d '{"name":"Ada Okafor","email":"ada@example.com","department":"Computer Science","level":200}'
#
# The exact curl command may need adjustment depending on the operating
# system's terminal and quoting rules.
#
# ------------------------------------------------
# 18. HOW A REACT FRONTEND USES THE API
# ------------------------------------------------
#
# A React frontend can request the student list using fetch:
#
# fetch("http://127.0.0.1:8000/api/students/")
#     .then((response) => {
#         if (!response.ok) {
#             throw new Error("The API request failed");
#         }
#         return response.json();
#     })
#     .then((data) => {
#         console.log(data);
#     })
#     .catch((error) => {
#         console.error(error);
#     });
#
# This example is JavaScript for a React project, not Python. Copy it into
# an appropriate React component or test file, not into this .py guide.
#
# If React runs on a different origin or port, Django may need CORS
# configuration. Configure allowed frontend origins deliberately; do not
# disable security protections indiscriminately.
#
# ------------------------------------------------
# 19. BASIC API DESIGN CHECKLIST
# ------------------------------------------------
#
# Before calling an API complete, check:
#
# [ ] URLs use clear, consistent resource names.
# [ ] HTTP methods match the intended action.
# [ ] The API returns appropriate status codes.
# [ ] Serializers validate incoming data.
# [ ] Error responses are understandable.
# [ ] Only necessary fields are exposed.
# [ ] Authentication and permissions are configured for protected data.
# [ ] Secrets are stored in environment variables, not committed to Git.
# [ ] API endpoints are tested with valid and invalid data.
# [ ] The API is documented so frontend developers know how to use it.
#
# Additional topics to introduce after this lesson:
# - Pagination for large lists.
# - Filtering, searching, and ordering.
# - Authentication with JWT.
# - Role-based permissions.
# - Automated API tests.
# - API versioning and documentation.
#
# ------------------------------------------------
# 20. COMMON BEGINNER ERRORS AND SOLUTIONS
# ------------------------------------------------
#
# ERROR: "No module named rest_framework"
# SOLUTION: Activate the correct virtual environment and run:
#           pip install djangorestframework
#
# ERROR: "No such table"
# SOLUTION: Check the model, then run:
#           python manage.py makemigrations
#           python manage.py migrate
#
# ERROR: "404 Not Found"
# SOLUTION: Check the URL spelling, trailing slash, router registration,
#           and whether the ID exists.
#
# ERROR: "405 Method Not Allowed"
# SOLUTION: Check that the endpoint supports the HTTP method you selected.
#
# ERROR: "400 Bad Request"
# SOLUTION: Read the response body. It often explains which field failed
#           validation or which required field is missing.
#
# ERROR: Duplicate email rejected
# SOLUTION: This is expected because email is unique. Use a different email
#           address or update the existing student.
#
# ERROR: React cannot call the API
# SOLUTION: Confirm Django is running, verify the URL, inspect the browser
#           console and network tab, and check CORS configuration if needed.
#
# ------------------------------------------------
# 21. CLASS PRACTICAL EXERCISE
# ------------------------------------------------
#
# TASK:
# Extend the Student API.
#
# 1. Add a "phone_number" field to the Student model.
# 2. Create and apply a migration.
# 3. Add the new field to StudentSerializer.
# 4. Create a student with a phone number.
# 5. Retrieve the student using GET.
# 6. Update the department using PATCH.
# 7. Try to create a student with an invalid email.
# 8. Record the HTTP status code for each request.
#
# TEACHER'S NOTE:
# When adding a new field to an existing model, Django may ask how to handle
# existing rows if the field is required. Explain defaults and nullability
# before students choose a migration option. Avoid blindly accepting a
# default without understanding what it means.
#
# ------------------------------------------------
# 22. OBJECTIVE QUESTIONS
# ------------------------------------------------
#
# Choose the ONE best answer for each question.
#
# 1. What does API stand for?
#    A. Application Programming Interface
#    B. Applied Program Internet
#    C. Automatic Python Installation
#    D. Application Process Integration
#
# 2. What is the main purpose of an API in a React + Django application?
#    A. To replace the database
#    B. To allow the frontend and backend to communicate
#    C. To style React components
#    D. To compile Python code into HTML
#
# 3. Which HTTP method is normally used to retrieve data?
#    A. POST
#    B. DELETE
#    C. GET
#    D. PATCH
#
# 4. Which HTTP method is commonly used to create a resource?
#    A. POST
#    B. GET
#    C. DELETE
#    D. TRACE
#
# 5. Which method is commonly used for a partial update?
#    A. GET
#    B. PATCH
#    C. DELETE
#    D. OPTIONS
#
# 6. What does a serializer do in Django REST Framework?
#    A. Only creates HTML pages
#    B. Converts model data to API-friendly representations and validates input
#    C. Starts the development server
#    D. Creates the database engine
#
# 7. Which status code commonly indicates that a resource was created?
#    A. 200
#    B. 201
#    C. 404
#    D. 500
#
# 8. Which status code means the requested resource was not found?
#    A. 201
#    B. 204
#    C. 404
#    D. 500
#
# 9. Which URL is the clearest REST-style endpoint for a student collection?
#    A. /api/getAllStudents/
#    B. /api/students/
#    C. /api/doStudent/
#    D. /api/studentAction/
#
# 10. What does a Django model mainly define?
#     A. The database structure and fields
#     B. The React page layout
#     C. The HTTP method names
#     D. The browser's address bar
#
# 11. What command creates migration files after a model change?
#     A. python manage.py runserver
#     B. python manage.py makemigrations
#     C. python manage.py startapp
#     D. pip freeze
#
# 12. What command applies migrations to the database?
#     A. python manage.py migrate
#     B. python manage.py collectstatic
#     C. python manage.py shell
#     D. python manage.py createsuperuser
#
# 13. Which HTTP method is normally used to delete a resource?
#     A. GET
#     B. POST
#     C. DELETE
#     D. PATCH
#
# 14. What does a 400 Bad Request response commonly indicate?
#     A. The request data is invalid
#     B. The server has restarted successfully
#     C. A new record was created
#     D. The requested record was deleted
#
# 15. Why should a real student API use authentication and permissions?
#     A. To make every endpoint public
#     B. To help restrict access to authorized users
#     C. To remove the need for validation
#     D. To avoid using a database
#
# ------------------------------------------------
# 23. ANSWER KEY FOR THE TEACHER
# ------------------------------------------------
#
# 1. A
# 2. B
# 3. C
# 4. A
# 5. B
# 6. B
# 7. B
# 8. C
# 9. B
# 10. A
# 11. B
# 12. A
# 13. C
# 14. A
# 15. B
#
# ------------------------------------------------
# 24. LESSON SUMMARY
# ------------------------------------------------
#
# Students have learned that:
# - An API allows applications to communicate.
# - RESTful APIs organize access around resources.
# - HTTP methods describe what the client wants to do.
# - HTTP status codes communicate the result.
# - Django models define stored data.
# - DRF serializers convert and validate data.
# - ViewSets provide common CRUD actions.
# - Routers help generate consistent API URLs.
# - API endpoints should be tested with both valid and invalid data.
#
# HOMEWORK:
# Build a simple Course API with fields:
# - course_name
# - course_code (unique)
# - duration_weeks
# - instructor_name
#
# Include list, create, retrieve, update, and delete operations.
# Test the API and submit screenshots or a short report showing:
# 1. The endpoint URLs.
# 2. One successful POST request.
# 3. One successful GET request.
# 4. One validation error.
# 5. The status codes received.
#
# END OF TEACHING GUIDE
