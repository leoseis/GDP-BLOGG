"""
DJANGO FOR BEGINNERS — PART 1
=============================
PROJECT: SIMPLE BLOG APPLICATION
FOCUS: Setup, project structure, apps, URLs/routing, views, templates, and requests.

HOW TO USE THIS FILE
--------------------
- Open this file in VS Code and teach from top to bottom.
- This is a teaching guide, not the Django application's source code.
- Commands and code examples are shown as lesson notes so this file can run safely.
- Type the actual commands in your terminal and put code snippets in the files indicated.
- Part 2 will add a database, a Post model, and CRUD operations.

LEARNING OBJECTIVES
-------------------
By the end of this lesson, students should be able to:
1. Explain what Django is and why it is used.
2. Create and activate a Python virtual environment.
3. Install Django and start a project.
4. Explain the difference between a Django project and an app.
5. Identify important files and folders.
6. Connect URL routes to views.
7. Return an HTTP response from a view.
8. Render an HTML template.
9. Run the development server and test pages in a browser.

============================================================
LESSON 1 — WHAT IS DJANGO?
============================================================

Django is a Python web framework. It gives us tools for building websites
without having to create every feature from scratch.

A simple request journey:
Browser -> URL route -> View -> Response -> Browser

Example:
A visitor opens /about/
Django checks the URL patterns.
Django finds the matching view.
The view returns a response.
The browser displays the response.

Important words:
- Project: the complete website configuration.
- App: one part of the website, such as a blog, users, or payments.
- URL route: the address that connects a browser request to a view.
- View: Python code that decides what response to send.
- Template: an HTML file used to display a page.
- Model: a Python class that describes database data. We will cover this in Part 2.

============================================================
LESSON 2 — PREPARE THE WORKING FOLDER
============================================================

Open the VS Code terminal.

STEP 1: Check Python
Run:
    python3 --version

If your system uses the command "python", use that instead.

STEP 2: Create a folder and enter it
Run:
    mkdir django_blog_course
    cd django_blog_course

STEP 3: Create a virtual environment
Run:
    python3 -m venv .venv

A virtual environment keeps this project's Python packages separate from
other projects on your computer.

STEP 4: Activate the environment

Linux / macOS:
    source .venv/bin/activate

Windows Command Prompt:
    .venv\\Scripts\\activate.bat

Windows PowerShell:
    .venv\\Scripts\\Activate.ps1

When activated, you will usually see (.venv) at the beginning of the terminal line.

STEP 5: Install Django
Run:
    python -m pip install django

STEP 6: Confirm installation
Run:
    python -m django --version

If you see a version number, Django is installed.

============================================================
LESSON 3 — CREATE THE DJANGO PROJECT
============================================================

Run this command inside django_blog_course:
    django-admin startproject config .

The dot at the end means: create the project files in the current folder.

Expected structure:
    django_blog_course/
        .venv/
        manage.py
        config/
            __init__.py
            settings.py
            urls.py
            asgi.py
            wsgi.py

What the important files do:
- manage.py: runs Django commands for this project.
- config/settings.py: project settings, installed apps, templates, database settings.
- config/urls.py: main URL routing file.
- config/asgi.py and config/wsgi.py: entry points used by hosting servers.
- __init__.py: tells Python this folder is a package.

The project folder is named "config" here, but you can choose another name.

============================================================
LESSON 4 — RUN THE STARTER WEBSITE
============================================================

Run:
    python manage.py runserver

Open this address in your browser:
    http://127.0.0.1:8000/

You should see Django's starter page.

To stop the server, click the terminal and press Ctrl+C.

Important:
- The development server is for local development, not production hosting.
- Keep the server running while testing pages in your browser.
- If the terminal says the port is already in use, stop the other server or use:
      python manage.py runserver 8001

============================================================
LESSON 5 — CREATE A BLOG APP
============================================================

A Django project can contain many apps. Our blog functionality will live in an
app called "blog".

Run:
    python manage.py startapp blog

The structure now includes:
    blog/
        __init__.py
        admin.py
        apps.py
        migrations/
        models.py
        tests.py
        views.py

What these files mean:
- admin.py: registers models for the Django admin site.
- apps.py: app configuration.
- migrations/: database-change history; important in Part 2.
- models.py: database models; we will edit it in Part 2.
- tests.py: automated tests.
- views.py: Python functions/classes that respond to requests.

STEP: Register the app
Open config/settings.py.
Find INSTALLED_APPS and add 'blog', for example:

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'blog',
    ]

Save the file.

Why register the app?
Django needs to know that the app is part of this project.

============================================================
LESSON 6 — CREATE YOUR FIRST VIEW
============================================================

Open blog/views.py and add:

    from django.http import HttpResponse

    def home(request):
        return HttpResponse("Welcome to my Django Blog!")

Explanation:
- import HttpResponse: brings in a response helper.
- def home(request): defines a view function.
- request: contains information about the browser request.
- return HttpResponse(...): sends text back to the browser.

A view must return a response. It should not simply print a message in the terminal.

============================================================
LESSON 7 — CONNECT URLS TO THE VIEW
============================================================

We will create app-level URLs, then connect them to the project's main URLs.

STEP 1: Create blog/urls.py
Django does not create this file automatically. Create it yourself.

Put this code in blog/urls.py:

    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.home, name='home'),
    ]

Explanation:
- path() defines a URL pattern.
- '' means the app's root path.
- views.home is the function Django should call.
- name='home' gives the route a reusable name.

STEP 2: Connect the app URLs to config/urls.py

Replace or update config/urls.py so it contains:

    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('blog.urls')),
    ]

Explanation:
- include('blog.urls') sends matching URL checks to the blog app.
- The empty prefix '' means the blog app handles the website root.
- Keep the admin route so you can use Django's admin site later.

STEP 3: Test it
Run:
    python manage.py runserver

Visit:
    http://127.0.0.1:8000/

You should see:
    Welcome to my Django Blog!

If you see a 404:
1. Check that blog is in INSTALLED_APPS.
2. Check that blog/urls.py exists.
3. Check the spelling of views.home.
4. Check that config/urls.py includes blog.urls.
5. Save your files and look at the terminal for error messages.

============================================================
LESSON 8 — CREATE A SECOND PAGE
============================================================

In blog/views.py, add:

    def about(request):
        return HttpResponse("This is the About page of my blog.")

In blog/urls.py, add another route:

    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.home, name='home'),
        path('about/', views.about, name='about'),
    ]

Test these addresses:
    http://127.0.0.1:8000/
    http://127.0.0.1:8000/about/

Notice:
- The browser URL is matched against urlpatterns.
- The trailing slash is conventional in Django routes.
- The route name ('about') can be used in templates rather than hard-coding a URL.

============================================================
LESSON 9 — USE AN HTML TEMPLATE
============================================================

Returning plain text is useful for learning, but real websites usually display HTML.

STEP 1: Create folders:
    blog/
        templates/
            blog/
                home.html
                about.html

The inner "blog" folder helps prevent template-name clashes between apps.

STEP 2: Put this in blog/templates/blog/home.html:

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My Django Blog</title>
    </head>
    <body>
        <h1>Welcome to My Django Blog</h1>
        <p>This is my first page rendered from a Django template.</p>
        <a href="{% url 'about' %}">About this blog</a>
    </body>
    </html>

STEP 3: Update blog/views.py:

    from django.shortcuts import render

    def home(request):
        return render(request, 'blog/home.html')

    def about(request):
        return render(request, 'blog/about.html')

Explanation:
- render() combines the request with a template and returns an HTTP response.
- 'blog/home.html' is the template path relative to a templates directory.
- {% url 'about' %} asks Django to generate the URL for the route named 'about'.

STEP 4: Create about.html in the same templates folder:

     

Test both pages in the browser.

============================================================
LESSON 10 — PASS DATA FROM A VIEW TO A TEMPLATE
============================================================

A view can send Python data to a template using a context dictionary.

Update blog/views.py:

    from django.shortcuts import render

    def home(request):
        context = {
            'blog_name': 'My Learning Blog',
            'author': 'Student Author',
        }
        return render(request, 'blog/home.html', context)

In home.html, display the data:

    <h1>Welcome to {{ blog_name }}</h1>
    <p>Author: {{ author }}</p>

Explanation:
- context is a Python dictionary.
- 'blog_name' and 'author' are keys.
- {{ blog_name }} and {{ author }} are Django template variables.
- The values come from the view; they are not Python variables created in HTML.

============================================================
LESSON 11 — DISPLAY A TEMPORARY LIST OF POSTS
============================================================

Before connecting a database in Part 2, we can display sample data stored in Python.

In blog/views.py:

    from django.shortcuts import render

    def home(request):
        posts = [
            {'title': 'My First Post', 'content': 'I am learning Django.'},
            {'title': 'Learning Python', 'content': 'Python helps power this blog.'},
            {'title': 'My Next Goal', 'content': 'Next I will learn databases and CRUD.'},
        ]
        return render(request, 'blog/home.html', {'posts': posts})

In home.html, use a loop:

    <h1>Latest Blog Posts</h1>

    {% for post in posts %}
        <article>
            <h2>{{ post.title }}</h2>
            <p>{{ post.content }}</p>
        </article>
    {% empty %}
        <p>No posts are available yet.</p>
    {% endfor %}

Explanation:
- {% for post in posts %} repeats the HTML for each item.
- {{ post.title }} displays a dictionary value.
- {% empty %} displays a message if the list is empty.
- This list is temporary. It resets when the code changes/restarts and is not a database.
- In Part 2, we will replace it with records stored in a database.

============================================================
LESSON 12 — REQUESTS, RESPONSES, AND COMMON ERRORS
============================================================

A browser sends a request. Django routes the request to a view. The view returns
a response such as an HTML page, text, JSON, or a redirect.

Common status codes:
- 200: request succeeded.
- 404: page or route was not found.
- 500: an error occurred in the server code.

Beginner troubleshooting:
- ImportError: check import statements and spelling.
- TemplateDoesNotExist: check the templates folder path and template name.
- 404 page: check URL patterns and trailing path.
- Server won't start: read the terminal error; check whether the port is in use.
- Changes not visible: save files and refresh the browser; check the terminal.

============================================================
PRACTICAL CHECKLIST — PART 1
============================================================

Students should demonstrate all of these:
[ ] Create and activate a virtual environment.
[ ] Install Django.
[ ] Create a project called config.
[ ] Create and register an app called blog.
[ ] Run the development server.
[ ] Create home and about views.
[ ] Create blog/urls.py and connect it to config/urls.py.
[ ] Create home.html and about.html templates.
[ ] Pass context data from a view to a template.
[ ] Display a list of temporary sample posts using a template loop.

============================================================
OBJECTIVE QUESTIONS — PART 1
============================================================

Choose ONE correct answer for each question.

1. What is Django?
   A. A database only
   B. A Python web framework
   C. A web browser
   D. A text editor

2. Which command creates a Django project in the current directory?
   A. python manage.py startapp blog
   B. pip remove django
   C. django-admin startproject config .
   D. python runserver

3. What is the purpose of a virtual environment?
   A. To create HTML pages
   B. To isolate project packages
   C. To replace Python
   D. To store images only

4. Which file contains the main project URL patterns?
   A. config/urls.py
   B. blog/models.py
   C. blog/admin.py
   D. manage.py

5. Which command creates a Django app named blog?
   A. django-admin run blog
   B. python manage.py startapp blog
   C. python manage.py makeblog
   D. pip install blog

6. Where do we normally write function-based views for the blog app?
   A. blog/views.py
   B. blog/urls.py
   C. config/asgi.py
   D. blog/tests.py only

7. What does HttpResponse do?
   A. Creates a database table
   B. Sends a response to the requester
   C. Installs Django
   D. Activates the virtual environment

8. What does include('blog.urls') do?
   A. Deletes the blog app
   B. Connects the blog app's URL patterns
   C. Creates a template
   D. Registers a database model

9. Which Django shortcut renders a template?
   A. print()
   B. input()
   C. render()
   D. install()

10. Which syntax displays a variable in a Django template?
    A. (( blog_name ))
    B. {{ blog_name }}
    C. <python>blog_name</python>
    D. ##blog_name##

11. Which syntax loops over posts in a Django template?
    A. {% for post in posts %}
    B. {{ for post in posts }}
    C. #for posts
    D. <loop posts>

12. What is the purpose of name='about' in a URL pattern?
    A. It names the database
    B. It gives the route a reusable name
    C. It creates a user account
    D. It changes the HTML title automatically

ANSWER KEY
----------
1-B, 2-C, 3-B, 4-A, 5-B, 6-A, 7-B, 8-B, 9-C, 10-B, 11-A, 12-B

PRACTICAL ASSIGNMENT
--------------------
Extend the blog:
1. Add a Contact page with a /contact/ URL.
2. Add a 'description' value to the home view's context.
3. Display the description in home.html.
4. Add at least four sample posts to the temporary list.
5. Add a message that appears when the post list is empty.

NEXT LESSON — PART 2
--------------------
We will create a Post model, configure the database, run migrations, use the
Django admin, and build Create, Read, Update, and Delete (CRUD) operations.
"""

# End of Part 1 teaching guide.
