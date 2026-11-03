"""
DJANGO FOR BEGINNERS — PART 2
=============================
PROJECT: SIMPLE BLOG APPLICATION
FOCUS: Database integration, models, migrations, admin, and CRUD operations.

IMPORTANT
---------
This guide continues Part 1. Use the same django_blog_course project and blog app.
Complete Part 1 first. Commands and code examples are lesson notes in this file;
type them into your terminal or the relevant Django files as instructed.

LEARNING OBJECTIVES
-------------------
By the end of this lesson, students should be able to:
1. Explain what a database and a Django model are.
2. Understand migrations and why they are needed.
3. Create a Post model.
4. Apply migrations to create database tables.
5. Register a model in Django admin.
6. Display database records on a page.
7. Build Create, Read, Update, and Delete (CRUD) operations.
8. Use Django forms and CSRF protection.
9. Test the full blog workflow in a browser.

============================================================
LESSON 1 — WHAT IS A DATABASE?
============================================================

A database stores information so that it remains available after the website
or computer is restarted.

Examples of blog data:
- Post title
- Post content
- Date created
- Date last updated

Part 1 used a Python list for sample posts. That list was only temporary.
A database lets us store posts persistently.

Django supports several databases. A new Django project commonly starts with
SQLite, which is suitable for learning and many small projects. PostgreSQL is
also widely used, especially for production applications.

For this beginner lesson, use the project's default SQLite database. We can
switch to PostgreSQL in a later lesson without changing the basic model/view idea.

============================================================
LESSON 2 — UNDERSTAND THE MODEL
============================================================

A Django model is a Python class that describes the structure of stored data.

Open blog/models.py and add:

    from django.db import models

    class Post(models.Model):
        title = models.CharField(max_length=200)
        content = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.title

Explanation:
- class Post(models.Model): defines a database model.
- title: short text, limited to 200 characters.
- content: longer text.
- created_at: automatically set when the post is first created.
- updated_at: automatically refreshed when the post is saved.
- __str__: controls how the object is represented in the admin and shell.

The model is a description of the data. The database table will be created by migrations.

============================================================
LESSON 3 — CREATE AND APPLY MIGRATIONS
============================================================

A migration is Django's record of a database structure change.

STEP 1: Create migration instructions
Run:
    python manage.py makemigrations

You should see Django report that it created a migration for Post.

STEP 2: Apply the migrations
Run:
    python manage.py migrate

This creates or updates database tables according to the migrations.

Remember:
- makemigrations: prepares migration files based on model changes.
- migrate: applies those changes to the database.

Whenever you make a change to a model, the usual workflow is:
    python manage.py makemigrations
    python manage.py migrate

Do not delete migration files or the database as a routine fix. Read the error
message first and understand what is wrong.

============================================================
LESSON 4 — REGISTER POSTS IN THE ADMIN SITE
============================================================

Open blog/admin.py and add:

    from django.contrib import admin
    from .models import Post

    admin.site.register(Post)

Create an admin account:
    python manage.py createsuperuser

Follow the prompts to enter a username, email if requested, and password.
The password does not appear as you type it in the terminal; that is normal.

Start the server:
    python manage.py runserver

Visit:
    http://127.0.0.1:8000/admin/

Sign in with the superuser account. You should see Posts.
Try adding a post, saving it, and opening it again.

Security note:
- Never share the superuser password.
- Do not use DEBUG=True or the development server as production security settings.
- Admin access should be restricted in a real deployment.

============================================================
LESSON 5 — DISPLAY POSTS FROM THE DATABASE (READ)
============================================================

Open blog/views.py. Replace the old temporary-list home view with:

    from django.shortcuts import render, get_object_or_404, redirect
    from .models import Post

    def home(request):
        posts = Post.objects.order_by('-created_at')
        return render(request, 'blog/home.html', {'posts': posts})

Explanation:
- Post.objects gives access to database queries for Post records.
- order_by('-created_at') sorts newest posts first.
- The minus sign means descending order.
- The queryset is passed to the template as posts.

Update blog/templates/blog/home.html to show database posts:

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My Django Blog</title>
    </head>
    <body>
        <h1>My Django Blog</h1>
        <p><a href="{% url 'post_create' %}">Write a new post</a></p>

        {% for post in posts %}
            <article>
                <h2><a href="{% url 'post_detail' post.pk %}">{{ post.title }}</a></h2>
                <p>{{ post.content|truncatewords:25 }}</p>
                <small>Published: {{ post.created_at }}</small>
                <p>
                    <a href="{% url 'post_update' post.pk %}">Edit</a> |
                    <a href="{% url 'post_delete' post.pk %}">Delete</a>
                </p>
            </article>
            <hr>
        {% empty %}
            <p>No posts yet. Create the first post!</p>
        {% endfor %}
    </body>
    </html>

Note: This template refers to URLs we will create in the next lessons. Complete
the remaining steps before testing the page.

============================================================
LESSON 6 — CREATE A FORM FOR NEW POSTS (CREATE)
============================================================

Django's ModelForm can build a form from a model.

Create a new file: blog/forms.py

Put this code in blog/forms.py:

    from django import forms
    from .models import Post

    class PostForm(forms.ModelForm):
        class Meta:
            model = Post
            fields = ['title', 'content']
            widgets = {
                'title': forms.TextInput(attrs={
                    'placeholder': 'Enter your post title'
                }),
                'content': forms.Textarea(attrs={
                    'placeholder': 'Write your post here',
                    'rows': 8
                }),
            }

Explanation:
- ModelForm connects a form to a model.
- fields lists the fields the visitor is allowed to submit.
- created_at and updated_at are not included because Django manages them.

Add this view to blog/views.py:

    from .forms import PostForm

    def post_create(request):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = PostForm()

        return render(request, 'blog/post_form.html', {
            'form': form,
            'page_title': 'Create a Blog Post',
        })

Explanation:
- GET normally displays an empty form.
- POST carries submitted form data.
- is_valid() checks the submitted data.
- form.save() creates the database record.
- redirect('home') sends the visitor back to the home page.
- If invalid, the same page is rendered with validation errors.

Create blog/templates/blog/post_form.html:

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ page_title }}</title>
    </head>
    <body>
        <h1>{{ page_title }}</h1>

        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Save Post</button>
        </form>

        <p><a href="{% url 'home' %}">Cancel and return home</a></p>
    </body>
    </html>

Why is {% csrf_token %} important?
It adds a security token that helps protect POST forms against cross-site request
forgery. Keep it in internal Django POST forms.

============================================================
LESSON 7 — VIEW A SINGLE POST (READ)
============================================================

Add this view to blog/views.py:

    def post_detail(request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})

Explanation:
- pk is the post's primary key, a unique database identifier.
- get_object_or_404 retrieves the record or returns a 404 page if it does not exist.

Create blog/templates/blog/post_detail.html:

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ post.title }}</title>
    </head>
    <body>
        <p><a href="{% url 'home' %}">Back to all posts</a></p>
        <article>
            <h1>{{ post.title }}</h1>
            <p>{{ post.content|linebreaks }}</p>
            <small>Created: {{ post.created_at }}</small>
            <p><a href="{% url 'post_update' post.pk %}">Edit this post</a></p>
        </article>
    </body>
    </html>

The linebreaks filter converts line breaks in the text into HTML paragraph/line-break
formatting. Django templates escape ordinary text by default, helping protect against
HTML injection.

============================================================
LESSON 8 — UPDATE AN EXISTING POST (UPDATE)
============================================================

Add this view to blog/views.py:

    def post_update(request, pk):
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)

        return render(request, 'blog/post_form.html', {
            'form': form,
            'page_title': 'Edit Blog Post',
        })

What is instance=post?
- Without instance=post, form.save() creates a new post.
- With instance=post, the form edits the existing post.

The GET request fills the form with the current title and content.
The POST request validates and saves the changes.

============================================================
LESSON 9 — DELETE A POST (DELETE)
============================================================

For safety, use a confirmation page and delete only after a POST request.

Add this view to blog/views.py:

    def post_delete(request, pk):
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            post.delete()
            return redirect('home')

        return render(request, 'blog/post_confirm_delete.html', {'post': post})

Create blog/templates/blog/post_confirm_delete.html:

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Delete Post</title>
    </head>
    <body>
        <h1>Delete Post</h1>
        <p>Are you sure you want to delete "{{ post.title }}"?</p>

        <form method="post">
            {% csrf_token %}
            <button type="submit">Yes, delete this post</button>
        </form>

        <p><a href="{% url 'post_detail' post.pk %}">Cancel</a></p>
    </body>
    </html>

Important:
- Do not delete data through a GET link.
- GET should display the confirmation page.
- POST performs the destructive action.
- A real application should also check that the current user has permission to
  edit or delete that post. This beginner version does not yet include user ownership.

============================================================
LESSON 10 — CONNECT ALL BLOG URLS
============================================================

Open blog/urls.py and update it to:

    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.home, name='home'),
        path('about/', views.about, name='about'),
        path('posts/new/', views.post_create, name='post_create'),
        path('posts/<int:pk>/', views.post_detail, name='post_detail'),
        path('posts/<int:pk>/edit/', views.post_update, name='post_update'),
        path('posts/<int:pk>/delete/', views.post_delete, name='post_delete'),
    ]

Explanation:
- <int:pk> captures an integer from the URL and passes it to the view as pk.
- For example, /posts/3/ opens the post whose primary key is 3.
- Named routes make it easier to generate links using {% url ... %}.

Check that config/urls.py still includes the blog app:

    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('blog.urls')),
    ]

============================================================
LESSON 11 — COMPLETE blog/views.py EXAMPLE
============================================================

Use this as a reference for the imports and views. If you copy it, ensure that
blog/forms.py and all templates described earlier exist.

    from django.shortcuts import render, get_object_or_404, redirect
    from .models import Post
    from .forms import PostForm

    def home(request):
        posts = Post.objects.order_by('-created_at')
        return render(request, 'blog/home.html', {'posts': posts})

    def about(request):
        return render(request, 'blog/about.html')

    def post_create(request):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = PostForm()

        return render(request, 'blog/post_form.html', {
            'form': form,
            'page_title': 'Create a Blog Post',
        })

    def post_detail(request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})

    def post_update(request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)

        return render(request, 'blog/post_form.html', {
            'form': form,
            'page_title': 'Edit Blog Post',
        })

    def post_delete(request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            post.delete()
            return redirect('home')
        return render(request, 'blog/post_confirm_delete.html', {'post': post})

============================================================
LESSON 12 — RUN AND TEST THE COMPLETE APPLICATION
============================================================

Run these commands from the folder containing manage.py:

    python manage.py makemigrations
    python manage.py migrate
    python manage.py check
    python manage.py runserver

Open:
    http://127.0.0.1:8000/

Test the complete workflow:
1. Click "Write a new post".
2. Enter a title and content, then save.
3. Confirm the post appears on the home page.
4. Click the title to open the detail page.
5. Click Edit, change the content, and save.
6. Confirm the updated content is displayed.
7. Click Delete.
8. Confirm the page asks whether you want to delete the post.
9. Confirm deletion.
10. Visit /admin/ and verify the post is no longer listed.

CRUD means:
- Create: add a new post.
- Read: list posts and open one post.
- Update: edit an existing post.
- Delete: remove a post after confirmation.

============================================================
COMMON ERRORS AND HOW TO CHECK THEM
============================================================

1. "no such table: blog_post"
   Likely cause: migrations have not been applied.
   Try:
       python manage.py makemigrations
       python manage.py migrate

2. "TemplateDoesNotExist"
   Check the folder path, for example:
       blog/templates/blog/home.html
   Check that the view uses the same template name.

3. "NoReverseMatch"
   A template refers to a route name Django cannot find.
   Check blog/urls.py and the exact name used in {% url ... %}.

4. "NameError: PostForm is not defined"
   Check the import:
       from .forms import PostForm
   Also confirm blog/forms.py exists.

5. "ImportError" or "cannot import name"
   Check filenames, spelling, and whether the required class/function exists.

6. The post does not update
   Check that the update form uses:
       PostForm(request.POST, instance=post)

7. The delete action gives a CSRF error
   Confirm that the POST form includes:
       {% csrf_token %}

8. The server displays an error
   Read the traceback in the terminal. The last lines usually identify the file
   and line where the error occurred.

============================================================
PRACTICAL CHECKLIST — PART 2
============================================================

[ ] Create the Post model.
[ ] Run makemigrations and migrate.
[ ] Register Post in the admin.
[ ] Create a superuser and add a post through /admin/.
[ ] Display posts from the database.
[ ] Create a post using a form.
[ ] View one post.
[ ] Update an existing post.
[ ] Delete a post only after confirmation.
[ ] Test all CRUD actions in the browser.

============================================================
OBJECTIVE QUESTIONS — PART 2
============================================================

Choose ONE correct answer for each question.

1. What is a Django model used for?
   A. Describing data stored in the database
   B. Styling HTML only
   C. Starting the browser
   D. Creating a URL automatically in every case

2. Which field is suitable for a long blog post body?
   A. BooleanField
   B. TextField
   C. IntegerField
   D. DateField

3. What does makemigrations do?
   A. Applies changes to the database immediately
   B. Creates migration files based on model changes
   C. Deletes all records
   D. Starts the server

4. What does migrate do?
   A. Applies migrations to the database
   B. Creates a template
   C. Opens the admin page
   D. Installs Python

5. Which file is commonly used to register a model in Django admin?
   A. blog/views.py
   B. blog/admin.py
   C. config/asgi.py
   D. blog/urls.py

6. What does Post.objects.order_by('-created_at') do?
   A. Deletes all posts
   B. Sorts posts by created_at with newest first
   C. Creates a new post
   D. Changes every title

7. What is CRUD?
   A. Create, Read, Update, Delete
   B. Copy, Run, Upload, Download
   C. Create, Render, Use, Deploy
   D. Connect, Route, Update, Debug

8. What does form.is_valid() do?
   A. Checks whether submitted form data passes validation
   B. Starts the database
   C. Creates a URL
   D. Deletes the form

9. Why do we use {% csrf_token %} in an internal POST form?
   A. To add a page title
   B. To help protect against cross-site request forgery
   C. To create a model
   D. To format dates

10. What does get_object_or_404(Post, pk=pk) do?
    A. Always creates a post
    B. Gets the post or returns a 404 response if it is missing
    C. Deletes the post
    D. Creates a migration

11. What does instance=post do in a ModelForm?
    A. Makes the form edit the existing post
    B. Makes the post invisible
    C. Creates a new app
    D. Starts the development server

12. Why should deletion be performed by a POST request rather than a GET link?
    A. GET requests are always slower
    B. Deletion changes data and should not happen just by visiting a link
    C. POST requests do not need validation
    D. GET cannot display HTML

ANSWER KEY
----------
1-A, 2-B, 3-B, 4-A, 5-B, 6-B, 7-A, 8-A, 9-B, 10-B, 11-A, 12-B

FINAL PRACTICAL ASSIGNMENT
--------------------------
Build a simple blog website using the skills from Parts 1 and 2.

Requirements:
1. Create at least five blog posts.
2. Show all posts on the home page, newest first.
3. Open each post on its own detail page.
4. Add a Create Post form.
5. Add an Edit Post form.
6. Add a Delete confirmation page.
7. Add an About page.
8. Use clear headings and links to move between pages.
9. Test what happens if a visitor opens a post ID that does not exist.
10. Explain the request flow: URL -> view -> model/database (where needed) -> template -> response.

OPTIONAL CHALLENGES
-------------------
- Add a category field to Post.
- Add a published BooleanField.
- Display only published posts on the home page.
- Add basic CSS styling.
- Later, add login and permissions so only authorized authors can edit or delete posts.

SECURITY AND NEXT STEPS
-----------------------
This is a teaching project. Before using it publicly, add authentication and
authorization, ensure only permitted users can edit/delete records, configure
production settings, use secure environment variables, and deploy with a proper
production server and database.
"""

# End of Part 2 teaching guide.
