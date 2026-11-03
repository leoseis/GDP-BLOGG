# ================================================================
# NIIT BACKEND DEVELOPMENT TEACHING GUIDE
# TOPIC 1: INTRODUCTION TO REST APIs AND HTTP FUNDAMENTALS
# ================================================================
#
# COURSE OBJECTIVE:
# Equip students with the skills to design, implement, test, and secure
# RESTful APIs. This first lesson introduces REST APIs and HTTP fundamentals.
#
# HOW TO USE THIS FILE:
# - Open this .py file in VS Code.
# - Teach the notes from top to bottom.
# - All teaching notes and code examples are comments, so this guide itself
#   can be opened or run without executing the examples.
# - When a section asks students to create a Django file, copy only the
#   relevant code into that file in the actual Django project.
#
# LESSON OUTCOMES
# By the end of this lesson, students should be able to:
# 1. Explain what an API is and why applications use APIs.
# 2. Explain REST and identify the basic ideas behind RESTful APIs.
# 3. Explain the client-server request/response cycle.
# 4. Describe HTTP requests, responses, headers, bodies, and URLs.
# 5. Identify common HTTP methods and status codes.
# 6. Explain JSON and recognize JSON data.
# 7. Make a simple request to a public API using Python requests.
# 8. Understand how this foundation connects to Django REST Framework.
#
# ================================================================
# SECTION 1: WHAT IS AN API?
# ================================================================
#
# API stands for Application Programming Interface.
#
# In simple terms, an API is a way for two software applications to
# communicate and exchange information.
#
# REAL-LIFE EXAMPLE:
# Imagine ordering food through a delivery app:
# 1. You choose food in the app.
# 2. The app sends your order to the service that handles orders.
# 3. That service processes the request.
# 4. The service sends back a response.
#
# A web API works in a similar way. It receives a request and sends back
# data or a result.
#
# SOFTWARE EXAMPLE:
# A school portal has:
# - React frontend: the pages and buttons students use.
# - Django backend: the application logic.
# - Database: where student, course, and result records are stored.
#
# The React frontend can request student information from the Django API.
# The Django backend retrieves the information and returns it to React.
#
# React frontend ---> HTTP request ---> Django API ---> Database
# React frontend <--- JSON response <--- Django API <--- Database
#
# WHY NOT LET REACT CONNECT DIRECTLY TO THE DATABASE?
# The backend controls access, applies business rules, validates information,
# and protects data. Database credentials should not be exposed in frontend
# code.
#
# CLASS QUESTION:
# In a school portal, which part should normally validate a new student's
# information before it is saved: the frontend, the backend, or both?
#
# TEACHING POINT:
# Both can validate for a better user experience, but backend validation is
# essential because clients can send requests without using the frontend UI.
#
# ================================================================
# SECTION 2: WHAT IS REST?
# ================================================================
#
# REST stands for Representational State Transfer.
#
# REST is an architectural style used to guide the design of web services.
# A RESTful API commonly:
# - Organizes information around resources.
# - Uses HTTP methods to work with those resources.
# - Uses clear URLs to identify resources.
# - Exchanges representations of data, often JSON.
# - Uses HTTP status codes to communicate outcomes.
#
# WHAT IS A RESOURCE?
# A resource is a thing or collection of things an API manages.
#
# Examples:
# - students
# - courses
# - teachers
# - books
# - blog posts
# - announcements
#
# Imagine a school API. Its resources could include:
#
# /api/students/
# /api/courses/
# /api/teachers/
#
# These URLs describe the resources. HTTP methods determine what action the
# client is asking to perform.
#
# IMPORTANT:
# REST is not a programming language or a Django package. It is a set of
# design principles. Django REST Framework is a Python toolkit that helps
# developers build web APIs, including APIs that follow REST conventions.
#
# ================================================================
# SECTION 3: UNDERSTANDING CLIENT, SERVER, REQUEST, AND RESPONSE
# ================================================================
#
# CLIENT:
# The application or device making a request. Examples include a browser,
# a React application, a mobile app, Postman, or a Python script.
#
# SERVER:
# The application that receives and processes the request. In our course,
# Django will act as the backend server.
#
# REQUEST:
# A message sent by the client asking the server to do something.
#
# RESPONSE:
# The message the server sends back after processing the request.
#
# EXAMPLE:
# A browser requests:
# GET http://127.0.0.1:8000/api/students/
#
# The Django API may respond with:
# HTTP status: 200 OK
# Content-Type: application/json
#
# [
#     {
#         "id": 1,
#         "name": "Ada Okafor",
#         "department": "Computer Science"
#     }
# ]
#
# REQUEST/RESPONSE FLOW:
# 1. The client sends an HTTP request.
# 2. The server receives the request.
# 3. The backend processes the request and may query the database.
# 4. The server creates an HTTP response.
# 5. The client reads the response and displays or uses the data.
#
# ================================================================
# SECTION 4: WHAT IS HTTP?
# ================================================================
#
# HTTP stands for Hypertext Transfer Protocol.
#
# It is a protocol used for communication between web clients and servers.
# HTTPS is HTTP protected by encryption using TLS.
#
# An HTTP request commonly contains:
# - Method: what operation the client wants to perform.
# - URL/path: the resource being requested.
# - Headers: extra information about the request.
# - Body: optional data sent to the server.
#
# An HTTP response commonly contains:
# - Status code: the outcome of the request.
# - Headers: extra information about the response.
# - Body: the returned content, if any.
#
# EXAMPLE REQUEST:
#
# POST /api/students/ HTTP/1.1
# Content-Type: application/json
#
# {
#     "name": "Ada Okafor",
#     "department": "Computer Science"
# }
#
# EXPLANATION:
# - POST is the method.
# - /api/students/ is the path.
# - Content-Type tells the server the format of the submitted body.
# - The JSON body contains the data the client wants to submit.
#
# EXAMPLE RESPONSE:
#
# HTTP/1.1 201 Created
# Content-Type: application/json
#
# {
#     "id": 1,
#     "name": "Ada Okafor",
#     "department": "Computer Science"
# }
#
# ================================================================
# SECTION 5: UNDERSTANDING URLS AND ENDPOINTS
# ================================================================
#
# A URL identifies a location or resource on a network.
#
# Example:
# http://127.0.0.1:8000/api/students/
#
# Breakdown:
# - http://       Protocol
# - 127.0.0.1     Local computer address
# - 8000          Port where the development server is listening
# - /api/         API URL prefix
# - students/     Resource collection
#
# An endpoint is a particular API URL used to access a resource or operation.
#
# Examples:
# GET /api/students/       Request the student collection
# GET /api/students/1/     Request student with ID 1
#
# The URL alone does not tell the whole story. The HTTP method matters too.
# For example, GET /api/students/ reads the collection, while POST to the same
# endpoint commonly creates a new student.
#
# ================================================================
# SECTION 6: HTTP METHODS — THE FUNDAMENTALS
# ================================================================
#
# GET:
# Retrieve information. It should not be used to create, update, or delete
# database records.
#
# POST:
# Submit data, commonly to create a new resource.
#
# PUT:
# Replace or fully update an existing resource. Required fields usually need
# to be supplied.
#
# PATCH:
# Partially update a resource by supplying only the fields to change.
#
# DELETE:
# Delete a resource.
#
# EXAMPLE FOR A STUDENT API:
#
# GET     /api/students/       List students
# POST    /api/students/       Create a student
# GET     /api/students/5/     Retrieve student 5
# PUT     /api/students/5/     Fully update student 5
# PATCH   /api/students/5/     Change selected fields for student 5
# DELETE  /api/students/5/     Delete student 5
#
# MEMORY TIP:
# GET = read
# POST = create
# PUT = replace/update fully
# PATCH = update partly
# DELETE = remove
#
# CLASS ACTIVITY:
# Ask students which method they would use to:
# 1. Display all courses.
# 2. Register a new student.
# 3. Change only a student's department.
# 4. Remove an outdated test record.
#
# Answers: GET, POST, PATCH, DELETE.
#
# ================================================================
# SECTION 7: HTTP STATUS CODES
# ================================================================
#
# Status codes tell the client how the server handled the request.
#
# COMMON SUCCESS CODES:
# 200 OK:
# The request succeeded. Common for successful GET and update responses.
#
# 201 Created:
# A new resource was created successfully.
#
# 204 No Content:
# The request succeeded, and the response has no body. Often used after
# a successful DELETE request.
#
# COMMON CLIENT ERROR CODES:
# 400 Bad Request:
# The request or submitted data is invalid.
#
# 401 Unauthorized:
# Authentication is missing or invalid.
#
# 403 Forbidden:
# The server refuses the request, often because the user lacks permission.
#
# 404 Not Found:
# The requested resource or endpoint could not be found.
#
# 405 Method Not Allowed:
# The endpoint does not support the HTTP method used.
#
# SERVER ERROR:
# 500 Internal Server Error:
# An unexpected problem occurred on the server.
#
# CLASS EXERCISE:
# Match the situation to the status code.
# A. Student successfully created.
# B. Student ID does not exist.
# C. Required email is invalid.
# D. User is not authenticated.
# E. Server encounters an unexpected bug.
#
# Answers: A = 201, B = 404, C = commonly 400, D = 401, E = 500.
#
# Note: Exact status codes can depend on the API's design and configuration.
#
# ================================================================
# SECTION 8: WHAT IS JSON?
# ================================================================
#
# JSON stands for JavaScript Object Notation.
# It is a text format commonly used to send structured data between APIs
# and clients. It is not limited to JavaScript; Python can read it too.
#
# EXAMPLE JSON OBJECT:
#
# {
#     "name": "Ada Okafor",
#     "age": 22,
#     "is_registered": true,
#     "courses": ["Python", "Django", "SQL"]
# }
#
# JSON RULES TO NOTICE:
# - Property names use double quotes.
# - Text values use double quotes.
# - Numbers do not need quotation marks.
# - true, false, and null are lowercase.
# - Lists use square brackets.
# - Objects use curly braces.
#
# COMMON MISTAKE:
# This is not valid JSON:
#
# {
#     'name': 'Ada'
# }
#
# JSON requires double quotes around property names and string values:
#
# {
#     "name": "Ada"
# }
#
# Content-Type: application/json is a common HTTP header used when sending
# JSON data in a request or response.
#
# ================================================================
# SECTION 9: PRACTICAL 1 — CALL A PUBLIC API USING PYTHON
# ================================================================
#
# Before building our own Django API, students can see how a client consumes
# an existing API.
#
# We will use JSONPlaceholder, a public demo API. Its data is for practice,
# not a real student database.
#
# STEP 1: Install the requests package in the active virtual environment:
#
# pip install requests
#
# STEP 2: Create a file named api_basics.py.
#
# STEP 3: Copy this code into api_basics.py (this is executable Python):
#
# import requests
#
# url = "https://jsonplaceholder.typicode.com/posts/1"
#
# try:
#     response = requests.get(url, timeout=10)
#
#     print("Status code:", response.status_code)
#     response.raise_for_status()
#
#     post = response.json()
#     print("Title:", post["title"])
#     print("Body:", post["body"])
#
# except requests.exceptions.RequestException as error:
#     print("The API request failed:", error)
#
# STEP 4: Run the file:
#
# python api_basics.py
#
# WHAT THE CODE DOES:
# - imports requests, a library for making HTTP requests.
# - stores the API URL in a variable.
# - sends a GET request.
# - prints the HTTP status code.
# - raise_for_status() raises an error for unsuccessful HTTP responses.
# - response.json() parses the JSON response into Python data.
# - the try/except block handles common request errors.
#
# IMPORTANT:
# The computer needs internet access for this public API example. If it fails,
# check the internet connection and try again later.
#
# ================================================================
# SECTION 10: PRACTICAL 2 — SEND A POST REQUEST TO A DEMO API
# ================================================================
#
# Add this in a separate file, or below the first example after you
# understand the GET request:
#
# import requests
#
# url = "https://jsonplaceholder.typicode.com/posts"
#
# new_post = {
#     "title": "Learning REST APIs",
#     "body": "I am practising HTTP POST requests.",
#     "userId": 1
# }
#
# try:
#     response = requests.post(url, json=new_post, timeout=10)
#     print("Status code:", response.status_code)
#     response.raise_for_status()
#     print("Response data:", response.json())
# except requests.exceptions.RequestException as error:
#     print("The API request failed:", error)
#
# JSONPlaceholder simulates creation and may return a new ID, but it does not
# permanently save the submitted post like a real production database would.
#
# ================================================================
# SECTION 11: HOW THIS CONNECTS TO DJANGO REST FRAMEWORK
# ================================================================
#
# The public API exercises teach us how to consume an API.
# In later practical work, we will create our own API with Django REST
# Framework (DRF).
#
# A typical DRF application contains:
#
# models.py:
# Defines database models and fields.
#
# serializers.py:
# Converts model instances to JSON-compatible data and validates input.
#
# views.py:
# Handles requests and determines what response to return.
#
# urls.py:
# Connects URL patterns to views or ViewSets.
#
# settings.py:
# Holds project configuration, installed apps, middleware, and other settings.
#
# BASIC FLOW:
# Client request -> URL routing -> view -> serializer/model/database
# -> HTTP response -> client
#
# In a later lesson, we can build a Student API with endpoints such as:
#
# GET     /api/students/
# POST    /api/students/
# GET     /api/students/1/
# PATCH   /api/students/1/
# DELETE  /api/students/1/
#
# For this first lesson, students should understand the HTTP and REST
# foundations before building a complete API.
#
# ================================================================
# SECTION 12: INTRODUCTION TO GOOD API DESIGN
# ================================================================
#
# Good API design makes an API predictable and easier to use.
#
# 1. Use clear resource names:
#    Prefer /api/students/ over /api/getAllStudents/.
#
# 2. Use HTTP methods consistently:
#    GET reads, POST commonly creates, PATCH partially updates, DELETE removes.
#
# 3. Return meaningful status codes:
#    Do not return 200 for every outcome if a more accurate status applies.
#
# 4. Validate data on the backend:
#    Never trust data just because it came from your own frontend.
#
# 5. Return useful error messages:
#    Explain what went wrong without exposing secrets or internal tracebacks.
#
# 6. Protect private data:
#    Authentication verifies who a user is; permissions determine what that
#    user is allowed to do.
#
# 7. Use HTTPS in production:
#    HTTPS protects data in transit.
#
# 8. Keep secrets out of source code:
#    Store credentials and secret keys in environment variables or a suitable
#    secret manager.
#
# 9. Document endpoints:
#    Frontend developers need to know URLs, methods, request fields, responses,
#    and authentication requirements.
#
# 10. Test success and failure cases:
#     Test missing fields, invalid data, unknown IDs, and unsupported methods.
#
# SECURITY PREVIEW:
# CORS controls which browser-based origins may read responses from an API.
# CORS is not authentication and does not protect an API from every kind of
# client. A script or Postman can still send requests directly to a server.
#
# Rate limiting helps restrict how frequently clients can make requests.
# Input validation checks whether submitted data is acceptable.
# We will study these more deeply in the security lesson.
#
# ================================================================
# SECTION 13: COMMON BEGINNER ERRORS
# ================================================================
#
# ERROR: ModuleNotFoundError: No module named 'requests'
# FIX: Activate the correct virtual environment, then run:
#      pip install requests
#
# ERROR: Connection error or timeout
# FIX: Check internet access, URL spelling, and whether the API is available.
#
# ERROR: KeyError when accessing post["title"]
# FIX: Print the returned JSON first and check that the key exists. An API may
#      return an error object instead of the data expected.
#
# ERROR: Invalid JSON
# FIX: Check commas, quotation marks, braces, and the JSON format.
#
# ERROR: HTTP 404
# FIX: Confirm the endpoint URL and resource ID.
#
# ERROR: HTTP 405
# FIX: Check whether the endpoint supports the selected HTTP method.
#
# ERROR: HTTP 400
# FIX: Read the response body to see which input field or request detail is
#      invalid.
#
# ================================================================
# SECTION 14: CLASS PRACTICAL EXERCISES
# ================================================================
#
# EXERCISE A — CONCEPTS
# 1. Explain API in your own words.
# 2. Explain the difference between a client and a server.
# 3. Explain the difference between HTTP and HTTPS.
# 4. Give three examples of resources in a school portal.
# 5. Explain why a backend must validate data even when the frontend validates.
#
# EXERCISE B — HTTP METHODS
# For each task, write the most suitable HTTP method:
# 1. Display all blog posts.
# 2. Create a blog post.
# 3. Change only a post's title.
# 4. Replace all editable fields of a post.
# 5. Delete a test post.
#
# Suggested answers: GET, POST, PATCH, PUT, DELETE.
#
# EXERCISE C — STATUS CODES
# Identify the most suitable common status code:
# 1. Request succeeded.
# 2. Resource created.
# 3. Invalid submitted data.
# 4. Resource not found.
# 5. User has not authenticated.
#
# Suggested answers: 200, 201, 400, 404, 401.
#
# EXERCISE D — PYTHON API CLIENT
# 1. Run the GET example.
# 2. Print the complete JSON response.
# 3. Print only the post title.
# 4. Change the URL to request /posts/2.
# 5. Add a timeout to the request.
# 6. Explain what response.json() does.
#
# ================================================================
# SECTION 15: OBJECTIVE QUESTIONS
# ================================================================
#
# INSTRUCTION:
# Choose ONE best answer for each question.
#
# 1. What does API stand for?
#    A. Application Programming Interface
#    B. Automatic Program Installation
#    C. Applied Processing Internet
#    D. Application Python Instruction
#
# 2. What is the main purpose of an API?
#    A. To style a webpage
#    B. To allow software applications to communicate
#    C. To replace every database
#    D. To create a laptop operating system
#
# 3. What does REST stand for?
#    A. Remote Execution Software Transfer
#    B. Representational State Transfer
#    C. Response Server Technology
#    D. Resource Setup and Testing
#
# 4. Which of the following is an example of an API resource?
#    A. students
#    B. blue
#    C. 500
#    D. browser zoom
#
# 5. Which HTTP method is normally used to retrieve information?
#    A. POST
#    B. DELETE
#    C. GET
#    D. PATCH
#
# 6. Which HTTP method is commonly used to create a resource?
#    A. GET
#    B. POST
#    C. DELETE
#    D. OPTIONS
#
# 7. Which method is commonly used for a partial update?
#    A. PATCH
#    B. GET
#    C. DELETE
#    D. HEAD
#
# 8. What does HTTP 201 commonly mean?
#    A. The resource was not found
#    B. The server crashed
#    C. A resource was created
#    D. The user is unauthenticated
#
# 9. What does HTTP 404 commonly mean?
#    A. Created
#    B. Not Found
#    C. Forbidden
#    D. OK
#
# 10. Which format is commonly used to exchange structured data with APIs?
#     A. JSON
#     B. MP3
#     C. PNG
#     D. EXE
#
# 11. Which header commonly tells the server that a request body contains JSON?
#     A. Content-Type: application/json
#     B. Screen-Size: large
#     C. Browser-Name: Firefox
#     D. Database-Table: students
#
# 12. In a web application, which component should protect database credentials?
#     A. Public React code
#     B. The backend/server configuration
#     C. A public image file
#     D. The browser address bar
#
# 13. Which statement about HTTPS is correct?
#     A. It encrypts data in transit using TLS.
#     B. It automatically validates all submitted data.
#     C. It replaces the need for user permissions.
#     D. It makes every API endpoint public.
#
# 14. What does a 400 Bad Request response commonly indicate?
#     A. A resource was created successfully.
#     B. The request or submitted data is invalid.
#     C. The request was deleted.
#     D. The database has no tables, in every case.
#
# 15. What is the role of a client in the HTTP request/response cycle?
#     A. It always stores the server database.
#     B. It sends a request to a server.
#     C. It must be written in Python.
#     D. It replaces the HTTP protocol.
#
# ================================================================
# SECTION 16: ANSWER KEY FOR THE TEACHER
# ================================================================
#
# 1. A
# 2. B
# 3. B
# 4. A
# 5. C
# 6. B
# 7. A
# 8. C
# 9. B
# 10. A
# 11. A
# 12. B
# 13. A
# 14. B
# 15. B
#
# ================================================================
# SECTION 17: LESSON SUMMARY AND HOMEWORK
# ================================================================
#
# SUMMARY:
# - An API allows applications to communicate.
# - REST is an architectural style commonly used to design web APIs.
# - Resources represent the things an API manages.
# - HTTP requests carry methods, URLs, headers, and sometimes a body.
# - HTTP responses include a status code, headers, and sometimes a body.
# - GET, POST, PUT, PATCH, and DELETE have different purposes.
# - JSON is a common format for API data.
# - Python's requests library can consume an API.
# - Django REST Framework helps us build our own APIs.
# - Good APIs need validation, meaningful errors, testing, and security.
#
# HOMEWORK:
# 1. Write a short explanation of REST in your own words.
# 2. Draw a diagram showing a React client communicating with a Django API
#    and database.
# 3. Create a Python file that requests:
#    https://jsonplaceholder.typicode.com/posts/3
# 4. Print the status code and the post title.
# 5. Explain the difference between GET and POST.
# 6. Explain the difference between HTTP 401 and HTTP 403.
#
# NEXT TOPIC:
# REST architecture and endpoint design.
#
# END OF TOPIC 1
