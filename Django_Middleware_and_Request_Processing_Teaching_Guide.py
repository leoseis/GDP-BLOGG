# =============================================================================
# DJANGO BACKEND TEACHING GUIDE
# TOPIC: MIDDLEWARE AND REQUEST PROCESSING
# LEVEL: Beginner to early intermediate
# PROJECT: Django Blog
#
# HOW TO USE THIS FILE:
# Read the explanations and follow the numbered steps in class.
# All examples are comments so this remains a valid, non-executing .py guide.
# Copy the code examples into the actual Django project files when teaching.
# =============================================================================

# 1. LEARNING OBJECTIVES
# By the end of this lesson, students should be able to:
# - Explain requests and responses.
# - Explain middleware in simple terms.
# - Describe Django's request-response lifecycle.
# - Identify common built-in middleware.
# - Explain why middleware order matters.
# - Create, register, and test custom middleware.
# - Distinguish middleware from views.

# Ask students:
# "When a visitor opens our blog homepage, does Django go straight to the view?"
# Expected answer: No. The request passes through middleware first.

# 2. WHAT IS A REQUEST?
# A request is a message a client sends to a server asking it to do something.
# Examples:
# - A visitor opens the blog homepage.
# - A user submits a login form.
# - A mobile app asks the API for blog posts.
#
# A request commonly contains:
# - Method: GET, POST, PUT, PATCH, DELETE.
# - Path: for example, /posts/.
# - Headers: extra request information.
# - Body/data: information submitted by the client.
# - Cookies: small pieces of data sent by the browser.
#
# Example:
# A visitor opens http://127.0.0.1:8000/
# The browser sends a GET request to Django.

# 3. WHAT IS A RESPONSE?
# A response is what the server sends back after processing a request.
# It may contain an HTML page, JSON data, a redirect, or an error.
#
# Common status codes:
# 200 = OK
# 201 = Created
# 301/302 = Redirect
# 400 = Bad Request
# 401 = Authentication required/invalid
# 403 = Forbidden
# 404 = Not Found
# 500 = Internal Server Error
#
# Ask: "What status code is normally returned for a page that does not exist?"
# Answer: 404.

# 4. WHAT IS MIDDLEWARE?
# Middleware is a layer of code that processes requests and responses.
#
# Think of it as a security checkpoint or reception desk:
# before a visitor reaches the correct office (the view), the reception desk
# can inspect the visitor, apply rules, or record the visit.
#
# Middleware can:
# - Inspect or modify incoming requests.
# - Work with sessions and cookies.
# - Help protect the application.
# - Identify the logged-in user.
# - Add or modify response headers.
# - Record request information for debugging.
#
# Middleware is best for behaviour that applies across many requests.
# A particular post's business logic normally belongs in its view/application
# logic, not in middleware.

# 5. DJANGO REQUEST-RESPONSE LIFECYCLE
# Draw this flow on the board:
#
# Browser / Client
#       |
#       v
# HTTP Request
#       |
#       v
# Request Middleware (top to bottom)
#       |
#       v
# URL Resolver (checks urls.py)
#       |
#       v
# Matching View
#       |
#       v
# View performs the required work
#       |
#       v
# HTTP Response is created
#       |
#       v
# Response Middleware (bottom to top)
#       |
#       v
# Browser receives response
#
# Explain:
# 1. The visitor opens a URL.
# 2. The browser sends an HTTP request.
# 3. Request middleware processes it.
# 4. Django finds a matching URL pattern.
# 5. Django calls the matching view.
# 6. The view performs work, such as retrieving blog posts.
# 7. The view returns a response.
# 8. Response middleware processes the response.
# 9. The browser receives the final response.
#
# IMPORTANT:
# Request middleware runs in the order listed in MIDDLEWARE.
# Response middleware runs in reverse order.

# 6. BUILT-IN DJANGO MIDDLEWARE
# Open the project's settings.py and find the MIDDLEWARE list.
# A standard Django project includes entries similar to:
#
# MIDDLEWARE = [
#     "django.middleware.security.SecurityMiddleware",
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]
#
# Your project may contain extra entries. Do not delete them just to match
# this example.
#
# Explain the main middleware:
# SecurityMiddleware:
#     Applies security-related behaviour.
# SessionMiddleware:
#     Makes session data available through request.session.
# CommonMiddleware:
#     Provides common request/response behaviour.
# CsrfViewMiddleware:
#     Helps protect unsafe requests against CSRF attacks.
# AuthenticationMiddleware:
#     Makes the current user available through request.user.
# MessageMiddleware:
#     Supports temporary messages such as "Post saved".
# XFrameOptionsMiddleware:
#     Helps protect against certain clickjacking attacks.
#
# Ask: "Which middleware makes request.user available?"
# Answer: AuthenticationMiddleware.

# 7. WHY DOES MIDDLEWARE ORDER MATTER?
# Some middleware depends on other middleware.
# For example, AuthenticationMiddleware depends on session support.
# Therefore, SessionMiddleware must appear before AuthenticationMiddleware.
#
# Request direction:
#     Middleware A -> Middleware B -> Middleware C -> View
#
# Response direction:
#     View -> Middleware C -> Middleware B -> Middleware A
#
# Keep Django's default middleware in place. Add custom middleware carefully.
#
# Ask: "If A is listed before B, which one handles the response first?"
# Answer: B, because response processing is reversed.

# 8. PRACTICAL: CREATE CUSTOM MIDDLEWARE
# CLASSROOM SCENARIO:
# We want to record the HTTP method, requested path, and response status code.
#
# STEP 1:
# Find your Django app folder. In this example the app is named "blog".
#
# STEP 2:
# Create a file inside the app:
#     blog/middleware.py
#
# STEP 3:
# Add this code to blog/middleware.py:
#
# class RequestLoggingMiddleware:
#     def __init__(self, get_response):
#         # Django supplies the next processing step.
#         self.get_response = get_response
#
#     def __call__(self, request):
#         # This part runs before the view.
#         print("REQUEST METHOD:", request.method)
#         print("REQUEST PATH:", request.path)
#
#         # Pass the request to the next middleware or the view.
#         response = self.get_response(request)
#
#         # This part runs after the view returns a response.
#         print("RESPONSE STATUS:", response.status_code)
#
#         # Pass the response onward.
#         return response
#
# EXPLAIN THE CODE:
# __init__:
#     Django creates the middleware instance and supplies get_response.
# __call__:
#     Django calls this method for each request.
# request.method:
#     Gives the HTTP method, such as GET or POST.
# request.path:
#     Gives the path, such as / or /posts/.
# self.get_response(request):
#     Passes the request to the next step and receives its response.
# response.status_code:
#     Gives the response status code, such as 200 or 404.
# return response:
#     Sends the response onward. Do not forget this line.

# 9. REGISTER THE MIDDLEWARE
# Creating middleware.py is not enough. Django must be told to use it.
#
# STEP 1: Open the project's settings.py.
# STEP 2: Find MIDDLEWARE.
# STEP 3: Add the full import path:
#
#     "blog.middleware.RequestLoggingMiddleware",
#
# Example placement:
#
# MIDDLEWARE = [
#     "django.middleware.security.SecurityMiddleware",
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "blog.middleware.RequestLoggingMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]
#
# IMPORTANT:
# Use your actual app's Python package name. If the app is not called blog,
# replace "blog" with the correct name. Keep the existing default entries.

# 10. RUN AND TEST
# From the directory containing manage.py, run:
#
#     python manage.py check
#
# If the check succeeds, start the server:
#
#     python manage.py runserver
#
# Open:
#
#     http://127.0.0.1:8000/
#
# Look at the terminal. You should see output similar to:
#
#     REQUEST METHOD: GET
#     REQUEST PATH: /
#     RESPONSE STATUS: 200
#
# The status code depends on what your homepage returns.
#
# Visit another route, such as /about/, and check the terminal again.
# Visit a route that does not exist, such as /page-that-does-not-exist/.
# The middleware should record the request and normally show status 404.
#
# Django may print other server logs too. That is normal.

# 11. UNDERSTANDING THE REQUEST OBJECT
# Common Django HttpRequest attributes:
#
# request.method
#     HTTP method, such as GET or POST.
# request.path
#     Requested path, such as /posts/.
# request.GET
#     Query-string values in the URL.
# request.POST
#     Form values submitted using an HTML POST form.
# request.headers
#     Headers sent by the client.
# request.COOKIES
#     Cookies sent by the browser.
# request.user
#     Current user, made available by AuthenticationMiddleware.
# request.session
#     Session data, made available by SessionMiddleware.
#
# DRF NOTE:
# In Django REST Framework views, request.data is used to access parsed
# request content. It is provided by DRF's Request object; it is not the same
# as Django's request.POST.

# 12. MIDDLEWARE VS VIEWS
# Middleware:
# - Can run for many or all requests.
# - Runs before and after a view.
# - Is suitable for logging, security, sessions, and common processing.
#
# View:
# - Handles a particular URL/endpoint.
# - Performs the operation requested by the visitor.
# - May retrieve, create, update, or delete blog posts.
#
# Blog example:
# Middleware records that someone requested /posts/.
# The view retrieves posts from the database and returns the page.
#
# Ask: "Should creating a particular blog post happen in middleware?"
# Answer: No. That belongs in a view or application logic.

# 13. OPTIONAL EXTENSION: STOP A REQUEST
# Explain that middleware can return a response early without calling the view.
# This is only a classroom demonstration, not a complete security system.
#
# Add this example in blog/middleware.py only after the first example is clear:
#
# from django.http import HttpResponseForbidden
#
# class BlockSamplePathMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         if request.path == "/blocked/":
#             return HttpResponseForbidden(
#                 "This path is blocked for demonstration."
#             )
#
#         response = self.get_response(request)
#         return response
#
# Register it in settings.py using:
#     "blog.middleware.BlockSamplePathMiddleware",
#
# Visit /blocked/. Expected status: 403 Forbidden.
# Do not register this example until students understand the logging middleware.

# 14. OPTIONAL EXTENSION: FUNCTION-BASED MIDDLEWARE
# Django also supports function-based middleware.
# Teach this after the class-based version.
#
# def simple_middleware(get_response):
#     def middleware(request):
#         print("Request received:", request.path)
#         response = get_response(request)
#         print("Response sent:", response.status_code)
#         return response
#     return middleware
#
# Register it using:
#     "blog.middleware.simple_middleware",
#
# Do not register both logging examples at once unless you want to show that
# both middleware components run.

# 15. COMMON ERRORS AND FIXES
#
# ERROR: ModuleNotFoundError: No module named 'blog.middleware'
# Cause:
# - middleware.py is not inside the app folder.
# - The app package name or spelling is incorrect.
# Fix:
# - Check the file location and the import path in settings.py.
#
# ERROR: TypeError involving middleware arguments
# Cause:
# - The middleware class does not follow Django's expected structure.
# Fix:
# - Check __init__(self, get_response) and __call__(self, request).
#
# ERROR: Nothing prints in the terminal
# Cause:
# - Middleware was not registered.
# - Wrong import path.
# - Server was not restarted.
# Fix:
# - Save files, verify the import path, restart runserver, visit a URL.
#
# ERROR: Page stops working
# Cause:
# - Middleware did not return a response or raised an exception.
# Fix:
# - Make sure the normal path calls get_response(request) and returns response.
#
# ERROR: NameError: request is not defined
# Cause:
# - request is being used outside the method where Django supplies it.
# Fix:
# - Use request inside __call__(self, request).

# 16. SECURITY AND GOOD PRACTICES
# - Never print passwords, tokens, session IDs, or secret keys.
# - Avoid logging sensitive personal information.
# - Keep middleware focused on cross-request behaviour.
# - Return a response on every normal execution path.
# - Keep Django's security middleware enabled.
# - Do not remove CSRF middleware just to make a form work.
# - Test custom middleware before deployment.
#
# For production applications, use Python's logging module instead of relying
# on print statements. This lesson uses print only to make the concept visible.

# 17. PRACTICAL CLASSROOM TASK
# Students must:
# 1. Create middleware.py inside the blog app.
# 2. Create RequestLoggingMiddleware.
# 3. Print the request method.
# 4. Print the request path.
# 5. Call get_response(request).
# 6. Print the response status code.
# 7. Return the response.
# 8. Register middleware in settings.py.
# 9. Run python manage.py check.
# 10. Test the homepage and a second URL.
#
# Expected flow:
# Browser -> Middleware -> Blog View -> Response -> Middleware -> Browser

# 18. STUDENT EXERCISES
# 1. Explain middleware in your own words.
# 2. Name four built-in Django middleware components and state their purpose.
# 3. What is the difference between request.method and request.path?
# 4. Create middleware that prints "A visitor has entered the blog".
# 5. Modify it to print the response status code.
# 6. Visit a URL that does not exist. What status code do you expect?
# 7. Why should SessionMiddleware appear before AuthenticationMiddleware?
# 8. Explain one difference between middleware and a view.

# 19. OBJECTIVE QUESTIONS
#
# 1. What is middleware in Django?
#    A. A database table
#    B. A layer that processes requests and responses
#    C. A template file
#    D. A package manager
#
# 2. Which object represents an incoming HTTP request?
#    A. request
#    B. response
#    C. queryset
#    D. serializer
#
# 3. Which attribute gives the HTTP method?
#    A. request.path
#    B. request.user
#    C. request.method
#    D. response.status_code
#
# 4. Which attribute gives the requested URL path?
#    A. request.path
#    B. request.POST
#    C. request.headers
#    D. response.content
#
# 5. Which middleware makes request.user available?
#    A. CommonMiddleware
#    B. AuthenticationMiddleware
#    C. MessageMiddleware
#    D. SecurityMiddleware
#
# 6. Which middleware provides session support?
#    A. SessionMiddleware
#    B. CsrfViewMiddleware
#    C. CommonMiddleware
#    D. XFrameOptionsMiddleware
#
# 7. Where is middleware registered?
#    A. models.py
#    B. urls.py
#    C. settings.py
#    D. admin.py
#
# 8. What does get_response(request) do?
#    A. Deletes the request
#    B. Passes the request to the next step and receives a response
#    C. Creates a database
#    D. Starts the server
#
# 9. In what order does response processing pass through middleware?
#    A. Same order as request processing
#    B. Reverse order
#    C. Random order
#    D. Alphabetical order
#
# 10. Which status code means Not Found?
#     A. 200
#     B. 201
#     C. 403
#     D. 404
#
# 11. Where should the logic for creating a particular blog post normally live?
#     A. A view or application logic
#     B. Middleware only
#     C. settings.py
#     D. manage.py
#
# 12. What should normal custom middleware return?
#     A. The request object
#     B. The response object
#     C. The settings module
#     D. The database connection
#
# 13. Which method is commonly used to retrieve a page?
#     A. GET
#     B. DELETE
#     C. PATCH
#     D. TRACE
#
# 14. Which status code means Forbidden?
#     A. 200
#     B. 301
#     C. 403
#     D. 500
#
# 15. Which item should never be printed in ordinary request logs?
#     A. Request method
#     B. URL path
#     C. Password
#     D. Response status code

# 20. OBJECTIVE ANSWER KEY
# 1. B
# 2. A
# 3. C
# 4. A
# 5. B
# 6. A
# 7. C
# 8. B
# 9. B
# 10. D
# 11. A
# 12. B
# 13. A
# 14. C
# 15. C

# 21. LESSON SUMMARY
# Students should leave knowing:
# 1. A request travels from the client to Django.
# 2. Request middleware can run before the view.
# 3. The view performs the operation for the requested URL.
# 4. The response passes back through middleware in reverse order.
# 5. Middleware is registered in the MIDDLEWARE list in settings.py.
#
# FINAL CLASS QUESTION:
# "We want to record the method and path for every request before the view runs.
#  Should we repeat the code in every view or use middleware?"
#
# Expected answer:
# Use middleware, because the logging requirement applies across requests.
#
# END OF LESSON
# =============================================================================
