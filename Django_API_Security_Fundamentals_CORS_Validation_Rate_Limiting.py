# =============================================================================
# DJANGO API SECURITY FUNDAMENTALS
# CORS, INPUT VALIDATION, AND RATE LIMITING
# Practical project: Django Blog API
# =============================================================================
#
# HOW TO TEACH WITH THIS FILE
# 1. Read the explanations in order.
# 2. When a section names settings.py, views.py, or serializers.py, switch to
#    that real project file and add the example there.
# 3. Commands and code examples are comments here, so this remains a valid
#    Python teaching-notes file.
# 4. Adapt "blog" and model/field names to the project being used.
#
# LEARNING OBJECTIVES
# Students should be able to:
# - Explain why APIs need security controls.
# - Configure CORS with django-cors-headers.
# - Validate incoming data with DRF serializers.
# - Apply request throttling with DRF.
# - Test allowed origins, invalid data, and HTTP 429 responses.
#
# IMPORTANT:
# CORS, validation, and throttling are only layers of protection. They do not
# replace authentication, permissions, HTTPS, secure secrets, or monitoring.
#
# =============================================================================
# 1. INTRODUCTION TO API SECURITY
# =============================================================================
#
# SIMPLE EXPLANATION:
# API security means protecting an API from misuse, invalid data, and access
# that should not be allowed.
#
# Imagine our Blog API allows users to view, create, edit, and delete posts.
# What could happen if anyone could submit any data and send unlimited requests?
#
# Expected student answers:
# - Empty or unsuitable data could be stored.
# - A client could send too many requests and overload the application.
# - A browser website from an unapproved origin could try to read API responses.
# - Users might try to perform actions they are not authorized to perform.
#
# THREE TOPICS:
# CORS = controls which browser origins may read cross-origin responses.
# VALIDATION = checks whether submitted data follows the application's rules.
# RATE LIMITING = restricts how frequently a client can make requests.
#
# Analogy:
# CORS is like deciding which websites are allowed to read a response.
# Validation is like checking a form before accepting it.
# Rate limiting is like setting a usage limit for a service.
#
# =============================================================================
# 2. UNDERSTAND THE REQUEST FLOW
# =============================================================================
#
# Draw this simplified flow on the board:
#
# CLIENT -> DJANGO MIDDLEWARE -> DRF VIEW
#        -> AUTHENTICATION / PERMISSIONS
#        -> THROTTLING
#        -> SERIALIZER VALIDATION
#        -> BUSINESS LOGIC
#        -> DATABASE
#        -> RESPONSE
#
# This is a teaching overview, not an exact execution trace for every request.
# The exact order depends on Django middleware and DRF configuration.
#
# Ask: "Should we trust validation performed only by React?"
# Answer: No. A client can bypass the frontend and call the API directly.
# The backend must enforce its own validation rules.
#
# =============================================================================
# 3. CORS - CROSS-ORIGIN RESOURCE SHARING
# =============================================================================
#
# SIMPLE EXPLANATION:
# An origin consists of scheme + host + port.
#
# Examples:
# http://localhost:5173
# http://127.0.0.1:8000
# https://myblog.example.com
#
# These are different origins because their host, scheme, or port differs.
#
# Example classroom setup:
# React/Vite frontend: http://localhost:5173
# Django API:          http://127.0.0.1:8000
#
# The browser may block frontend JavaScript from reading the API response
# unless the Django server allows the frontend origin through CORS.
#
# VERY IMPORTANT:
# CORS is not authentication.
# CORS is mainly enforced by browsers. It does not stop Postman, curl, or
# another server from sending a request to your API.
# CORS does not decide whether a user is logged in or allowed to delete a post.
#
# =============================================================================
# 4. INSTALL THE CORS PACKAGE
# =============================================================================
#
# Activate your virtual environment, then run in the terminal:
#
#     pip install django-cors-headers
#     pip freeze > requirements.txt
#
# Explain that the package adds CORS support through Django middleware.
#
# =============================================================================
# 5. CONFIGURE CORS IN settings.py
# =============================================================================
#
# STEP A - Add the package to INSTALLED_APPS:
#
#     INSTALLED_APPS = [
#         # Existing Django apps...
#         "corsheaders",
#         "rest_framework",
#         # Your own apps...
#     ]
#
# STEP B - Add CorsMiddleware near the top of MIDDLEWARE, before
# CommonMiddleware:
#
#     MIDDLEWARE = [
#         "django.middleware.security.SecurityMiddleware",
#         "corsheaders.middleware.CorsMiddleware",
#         "django.middleware.common.CommonMiddleware",
#         # Other existing middleware...
#     ]
#
# STEP C - Allow only the frontend origins that need access:
#
#     CORS_ALLOWED_ORIGINS = [
#         "http://localhost:5173",
#         "http://127.0.0.1:5173",
#     ]
#
# Explain:
# - Include scheme, host, and port.
# - Do not include a URL path such as /api.
# - Do not add a trailing slash.
# - Add the real deployed frontend origin when deploying.
#
# AVOID THIS IN PRODUCTION UNLESS THERE IS A VERY SPECIFIC REASON:
#
#     CORS_ALLOW_ALL_ORIGINS = True
#
# It allows every origin to read responses in a browser. Prefer a specific
# allowlist of trusted frontend origins.
#
# If using cookies/session authentication across origins, configure credentials
# and CSRF protection carefully. CORS_ALLOWED_ORIGINS and
# CSRF_TRUSTED_ORIGINS serve different purposes; one does not replace the other.
#
# =============================================================================
# 6. TEST CORS
# =============================================================================
#
# 1. Start Django:
#       python manage.py runserver
#
# 2. Open the frontend from an allowed origin, e.g. http://localhost:5173.
#
# 3. Make a frontend request to:
#       http://127.0.0.1:8000/api/posts/
#
# 4. Inspect the browser Developer Tools -> Console and Network tabs.
#
# 5. Try an origin that is not in CORS_ALLOWED_ORIGINS. Browser JavaScript
#    should not be allowed to read the response.
#
# Remember: the request may still reach Django. The browser's CORS policy
# controls whether JavaScript can read the response; CORS is not a firewall.
#
# =============================================================================
# 7. INPUT VALIDATION - CHECKING SUBMITTED DATA
# =============================================================================
#
# SIMPLE EXPLANATION:
# Input validation checks whether incoming data is acceptable before it is
# saved or processed.
#
# Blog post rules could include:
# - title must not be blank.
# - title must not exceed the allowed length.
# - content must not contain only spaces.
# - fields must have the expected data types.
#
# DRF serializers are commonly used to:
# - Convert model objects into response data.
# - Read incoming request data.
# - Validate submitted values.
# - Save valid data.
#
# Do not rely only on frontend validation. A user can call the API directly.
#
# =============================================================================
# 8. REVIEW THE BLOG MODEL
# =============================================================================
#
# FILE: blog/models.py (or your app's models.py)
#
# Example only - use the model already in your project:
#
#     from django.db import models
#
#     class Post(models.Model):
#         title = models.CharField(max_length=200)
#         author = models.CharField(max_length=100)
#         content = models.TextField()
#         created_at = models.DateTimeField(auto_now_add=True)
#
# Explain:
# CharField(max_length=200) stores text with a maximum length.
# TextField stores longer text.
# Do not create a second Post model if one already exists.
#
# =============================================================================
# 9. CREATE OR REVIEW PostSerializer
# =============================================================================
#
# FILE: blog/serializers.py
#
# If serializers.py does not exist, create it inside the Django app folder.
#
#     from rest_framework import serializers
#     from .models import Post
#
#     class PostSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = Post
#             fields = [
#                 "id",
#                 "title",
#                 "author",
#                 "content",
#                 "created_at",
#             ]
#             read_only_fields = ["id", "created_at"]
#
# Explain:
# - ModelSerializer is connected to the Post model.
# - fields controls which fields are exposed by this serializer.
# - read_only_fields prevents clients from setting those fields on writes.
# If your model fields differ, change the list to match your model.
#
# =============================================================================
# 10. FIELD-LEVEL VALIDATION
# =============================================================================
#
# Add this method INSIDE PostSerializer in serializers.py:
#
#     def validate_title(self, value):
#         cleaned_title = value.strip()
#
#         if not cleaned_title:
#             raise serializers.ValidationError(
#                 "The title cannot be empty."
#             )
#
#         if len(cleaned_title) < 3:
#             raise serializers.ValidationError(
#                 "The title must contain at least 3 characters."
#             )
#
#         return cleaned_title
#
# Explain the naming rule:
# validate_<field_name>
#
# DRF calls validate_title when it validates the title field.
# Returning cleaned_title means the cleaned value is used.
#
# Add content validation too:
#
#     def validate_content(self, value):
#         cleaned_content = value.strip()
#
#         if not cleaned_content:
#             raise serializers.ValidationError(
#                 "The content cannot be empty."
#             )
#
#         return cleaned_content
#
# Ask: "What is the difference between validate_title and validate_content?"
# Answer: Each method validates a different serializer field.
#
# =============================================================================
# 11. OBJECT-LEVEL VALIDATION
# =============================================================================
#
# Object-level validation checks a rule involving more than one field.
# Example: title and content must not be exactly the same.
#
# Add this method INSIDE PostSerializer:
#
#     def validate(self, attrs):
#         title = attrs.get("title", "")
#         content = attrs.get("content", "")
#
#         if title.strip().lower() == content.strip().lower():
#             raise serializers.ValidationError(
#                 "The title and content must be different."
#             )
#
#         return attrs
#
# Explain:
# - validate_title checks one field.
# - validate checks the submitted fields together.
# - attrs contains values that passed field-level validation.
#
# For partial updates (PATCH), a field may be omitted. More advanced validation
# may need to use the existing instance value when a field is not submitted.
#
# =============================================================================
# 12. HOW THE VIEW USES SERIALIZER VALIDATION
# =============================================================================
#
# FILE: blog/views.py
#
# Example APIView for creating a post:
#
#     from rest_framework.views import APIView
#     from rest_framework.response import Response
#     from rest_framework import status
#     from .serializers import PostSerializer
#
#     class PostListCreateAPIView(APIView):
#         def post(self, request):
#             serializer = PostSerializer(data=request.data)
#
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(
#                     serializer.data,
#                     status=status.HTTP_201_CREATED
#                 )
#
#             return Response(
#                 serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
# Explain line by line:
# 1. request.data contains the incoming body.
# 2. The serializer receives that data.
# 3. is_valid() runs the validation rules.
# 4. save() stores valid data.
# 5. serializer.errors explains why invalid data was rejected.
#
# Never call serializer.save() before successful validation.
# If the project already uses ModelViewSet, keep that ViewSet and use the
# validated serializer there. Do not create a duplicate endpoint unnecessarily.
#
# =============================================================================
# 13. TEST INPUT VALIDATION
# =============================================================================
#
# Use Postman or Thunder Client.
#
# Example request:
#     POST http://127.0.0.1:8000/api/posts/
# Header:
#     Content-Type: application/json
#
# VALID JSON:
#     {
#         "title": "Learning API Security",
#         "author": "Student One",
#         "content": "This post explains validation."
#     }
#
# Expected: HTTP 201 Created if the endpoint and permissions allow creation.
#
# INVALID JSON - TITLE CONTAINS ONLY SPACES:
#     {
#         "title": "   ",
#         "author": "Student One",
#         "content": "This post explains validation."
#     }
#
# Expected: HTTP 400 Bad Request with a title error.
#
# INVALID JSON - TITLE TOO SHORT:
#     {
#         "title": "Hi",
#         "author": "Student One",
#         "content": "This post explains validation."
#     }
#
# Expected: HTTP 400 Bad Request.
#
# INVALID JSON - TITLE AND CONTENT ARE THE SAME:
#     {
#         "title": "Same text",
#         "author": "Student One",
#         "content": "Same text"
#     }
#
# Expected: HTTP 400 Bad Request.
#
# Ask: "Where should validation happen?"
# Answer: Frontend validation helps users, but backend validation enforces rules.
#
# =============================================================================
# 14. RATE LIMITING - CONTROL REQUEST FREQUENCY
# =============================================================================
#
# SIMPLE EXPLANATION:
# Rate limiting restricts how many requests a client can make in a period.
#
# Example: allow an anonymous client 20 requests per minute.
#
# Why use it?
# - Reduces accidental excessive requests.
# - Helps protect expensive endpoints.
# - Makes some forms of abuse more difficult.
# - Helps preserve service capacity for other clients.
#
# Important limitation:
# Rate limiting alone does not stop every denial-of-service attack. It is one
# application-level control, not a replacement for infrastructure protection.
#
# =============================================================================
# 15. CONFIGURE DRF THROTTLING
# =============================================================================
#
# FILE: settings.py
#
# Add this to REST_FRAMEWORK, or merge these keys into the dictionary that
# already exists. Do not create a second setting that overwrites your first.
#
#     REST_FRAMEWORK = {
#         "DEFAULT_THROTTLE_CLASSES": [
#             "rest_framework.throttling.AnonRateThrottle",
#             "rest_framework.throttling.UserRateThrottle",
#         ],
#         "DEFAULT_THROTTLE_RATES": {
#             "anon": "20/min",
#             "user": "100/min",
#         },
#     }
#
# Explain:
# - AnonRateThrottle applies to unauthenticated clients.
# - UserRateThrottle applies to authenticated users.
# - 20/min means 20 requests per minute.
# - These are classroom example limits, not universal production values.
#
# Choose production limits based on endpoint cost, expected usage, and capacity.
#
# =============================================================================
# 16. APPLY A THROTTLE TO ONE VIEW
# =============================================================================
#
# FILE: blog/views.py
#
# Example:
#
#     from rest_framework.views import APIView
#     from rest_framework.response import Response
#     from rest_framework.throttling import AnonRateThrottle
#
#     class PublicPostListAPIView(APIView):
#         throttle_classes = [AnonRateThrottle]
#
#         def get(self, request):
#             return Response({
#                 "message": "Blog posts are available."
#             })
#
# A custom rate can be created like this:
#
#     from rest_framework.throttling import AnonRateThrottle
#
#     class SmallAnonymousRateThrottle(AnonRateThrottle):
#         rate = "5/min"
#
# Then assign it to a view:
#
#     class SensitiveAPIView(APIView):
#         throttle_classes = [SmallAnonymousRateThrottle]
#
# These are separate examples. Define each class only once in your real file.
#
# =============================================================================
# 17. TEST RATE LIMITING
# =============================================================================
#
# 1. Start the server:
#       python manage.py runserver
#
# 2. Send requests repeatedly to a throttled endpoint.
#
# 3. After the configured limit is exceeded, DRF normally returns:
#       HTTP 429 Too Many Requests
#
# 4. Wait for the throttle window to pass, then test again.
#
# DRF throttling uses Django's cache. For production with multiple workers or
# servers, use a shared cache such as Redis. Local-memory cache is not shared
# between separate processes, so it cannot coordinate limits across servers.
#
# DRF throttling is not a replacement for a reverse proxy, API gateway, WAF,
# or infrastructure-level protection against high-volume attacks.
#
# =============================================================================
# 18. COMMON ERRORS AND TROUBLESHOOTING
# =============================================================================
#
# ERROR: ModuleNotFoundError: No module named 'corsheaders'
# FIX:
#     pip install django-cors-headers
# Check that the correct virtual environment is active.
#
# ERROR: Browser reports a CORS problem.
# CHECK:
# - corsheaders is in INSTALLED_APPS.
# - CorsMiddleware is in MIDDLEWARE.
# - CorsMiddleware appears before CommonMiddleware.
# - CORS_ALLOWED_ORIGINS contains the exact frontend origin.
# - Scheme, host, and port are correct.
#
# ERROR: Serializer returns errors.
# CHECK:
# - Read serializer.errors.
# - Check JSON field names.
# - Check that the request body is valid JSON.
# - Check validation method names and return statements.
#
# ERROR: Rate limiting does not appear to work.
# CHECK:
# - Throttle classes and rates are configured.
# - The request reaches a DRF view.
# - You are testing as the expected anonymous/authenticated client.
# - Cache settings are appropriate for your environment.
#
# ERROR: HTTP 429.
# This normally means the throttle limit has been exceeded. Wait for the
# configured window or adjust the limit deliberately.
#
# =============================================================================
# 19. SECURITY BEST PRACTICES
# =============================================================================
#
# 1. Validate all untrusted input on the backend.
# 2. Allow only the frontend origins that need browser access.
# 3. Do not treat CORS as authentication or authorization.
# 4. Use authentication and permissions to control user actions.
# 5. Apply throttling to public and expensive endpoints.
# 6. Use HTTPS in production.
# 7. Keep SECRET_KEY, database passwords, and API credentials out of source code.
# 8. Use environment variables or a secure secrets manager for secrets.
# 9. Keep Django and dependencies updated.
# 10. Never log passwords, access tokens, or other sensitive credentials.
#
# =============================================================================
# 20. PRACTICAL CLASSROOM DEMONSTRATION
# =============================================================================
#
# TASK A - CORS
# 1. Install django-cors-headers.
# 2. Add corsheaders to INSTALLED_APPS.
# 3. Add CorsMiddleware before CommonMiddleware.
# 4. Allow the class frontend origin.
# 5. Test the API request in the browser.
#
# TASK B - INPUT VALIDATION
# 1. Open serializers.py.
# 2. Add validate_title().
# 3. Add validate_content().
# 4. Test a valid POST request.
# 5. Test blank and too-short titles.
#
# TASK C - RATE LIMITING
# 1. Open settings.py.
# 2. Add DRF throttle classes and rates.
# 3. Restart the server.
# 4. Send repeated requests.
# 5. Observe the 429 response after the limit is exceeded.
#
# At the end, ask students which problem each control addresses.
#
# =============================================================================
# 21. QUICK REVISION
# =============================================================================
#
# CORS:
# Browser policy controlling which origins may read cross-origin responses.
#
# INPUT VALIDATION:
# Checks submitted data against application rules.
#
# RATE LIMITING:
# Restricts how often a client can make requests.
#
# AUTHENTICATION:
# Establishes who the user/client is.
#
# PERMISSIONS / AUTHORIZATION:
# Determines what that user is allowed to do.
#
# These controls solve different problems and should work together.
#
# =============================================================================
# 22. OBJECTIVE QUESTIONS
# =============================================================================
#
# Choose the best answer.
#
# 1. What does CORS stand for?
#    A. Cross-Origin Resource Sharing
#    B. Central Object Request System
#    C. Client-Origin Response Security
#    D. Cross-Object Routing Service
#
# 2. What is the main purpose of CORS?
#    A. Hash passwords
#    B. Control browser access to cross-origin responses
#    C. Create database tables
#    D. Validate model fields
#
# 3. Is CORS a replacement for authentication?
#    A. Yes
#    B. No
#    C. Only in development
#    D. Only for GET requests
#
# 4. Which package is commonly used for CORS in Django?
#    A. django-cors-headers
#    B. django-images
#    C. django-admin-tools
#    D. django-passwords-only
#
# 5. Where should CorsMiddleware be placed?
#    A. After all views
#    B. Before CommonMiddleware
#    C. Inside models.py
#    D. Inside serializers.py
#
# 6. Which setting lists allowed browser origins?
#    A. ALLOWED_HOSTS
#    B. CORS_ALLOWED_ORIGINS
#    C. STATIC_URL
#    D. MEDIA_ROOT
#
# 7. Why is backend validation necessary?
#    A. Frontend validation cannot be bypassed
#    B. Clients can call the API directly
#    C. It removes the database
#    D. It disables HTTP
#
# 8. Which method runs serializer validation?
#    A. serializer.is_valid()
#    B. serializer.run()
#    C. serializer.check_database()
#    D. serializer.validate_now()
#
# 9. Which method validates a field named title?
#    A. check_title()
#    B. validate_title()
#    C. title_is_valid()
#    D. clean_title_only()
#
# 10. Object-level validation is used to:
#     A. Check rules involving multiple fields
#     B. Start the server
#     C. Install Django
#     D. Create a URL
#
# 11. What should happen when serializer validation fails?
#     A. Save invalid data
#     B. Return validation errors, commonly HTTP 400
#     C. Delete the database
#     D. Restart the computer
#
# 12. What is rate limiting?
#     A. Limiting database tables
#     B. Restricting request frequency
#     C. Limiting serializers
#     D. Blocking every GET request
#
# 13. Which DRF throttle is for anonymous clients?
#     A. AnonRateThrottle
#     B. ModelRateThrottle
#     C. SerializerRateThrottle
#     D. AdminOnlyThrottle
#
# 14. What does "20/min" mean?
#     A. 20 requests per month
#     B. 20 requests per minute
#     C. 20 users per second
#     D. 20 database rows per minute
#
# 15. Which status code is normally returned when a DRF throttle limit is hit?
#     A. 200
#     B. 201
#     C. 404
#     D. 429
#
# =============================================================================
# 23. ANSWER KEY
# =============================================================================
#
# 1-A, 2-B, 3-B, 4-A, 5-B, 6-B, 7-B, 8-A, 9-B, 10-A,
# 11-B, 12-B, 13-A, 14-B, 15-D
#
# =============================================================================
# 24. PRACTICAL ASSIGNMENT
# =============================================================================
#
# Using the existing Blog API:
# 1. Configure CORS for the approved local frontend origin only.
# 2. Reject a blank title through serializer validation.
# 3. Reject content containing only spaces.
# 4. Configure anonymous clients for 10 requests per minute.
# 5. Test one valid POST request.
# 6. Test at least two invalid POST requests.
# 7. Exceed the rate limit and record the HTTP response.
# 8. Explain why CORS does not replace authentication.
#
# Submit:
# - Relevant settings.py configuration.
# - Serializer validation methods.
# - Evidence/notes from valid and invalid API tests.
# - A short explanation of CORS, validation, and throttling.
#
# =============================================================================
# END OF TEACHING GUIDE
# =============================================================================
