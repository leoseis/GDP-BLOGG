# DJANGO BLOG — PASSWORD HASHING AND SECURE CREDENTIAL STORAGE
# PRACTICAL STEP-BY-STEP BACKEND TEACHING GUIDE
# ================================================================
# Audience: Beginner Django backend students
# Practical project: Continue using the existing Django Blog project.
#
# IMPORTANT:
# This is a teaching reference file. Explanations, terminal commands,
# URLs and code examples are written as comments so this remains a
# valid Python file in VS Code.
#
# ================================================================
# 1. LESSON OBJECTIVES
# ================================================================
# By the end of this lesson, students should be able to:
# - Explain the difference between plaintext passwords and password hashes.
# - Explain why passwords should never be stored as readable text.
# - Understand how Django hashes and verifies passwords.
# - Create users safely with create_user().
# - Set or change passwords with set_password().
# - Verify passwords with check_password().
# - Authenticate users using Django's authentication system.
# - Configure basic password validation.
# - Identify unsafe credential-storage practices.
# - Apply these ideas to the existing Django Blog project.
#
# ================================================================
# 2. START WITH A SIMPLE REAL-LIFE EXAMPLE
# ================================================================
# Ask students:
# "If someone steals a database containing users' passwords, what
# should happen?"
#
# Explain:
# If the database stores passwords as normal readable text, an attacker
# can immediately read and use those passwords.
#
# A secure application does not store the original password.
# It stores a password hash produced by a password-hashing algorithm.
#
# Example:
#
#     User enters:       MyStrongPassword123!
#     Django stores:     pbkdf2_sha256$...$...$...
#
# The stored value is not the original password.
#
# IMPORTANT:
# A password hash is not encryption.
# Encryption is designed to be reversed with the correct key.
# Password hashing is designed to be one-way: the application verifies
# a password by checking it against the stored hash.
#
# ================================================================
# 3. HASHING VS ENCRYPTION
# ================================================================
# HASHING:
# - One-way process.
# - Used for password verification.
# - The original password is not meant to be recovered.
#
# ENCRYPTION:
# - Reversible when the correct decryption key is available.
# - Used when an application must later read protected data.
#
# TEACHING EXAMPLE:
# A Blog application needs to verify a user's password when they log in.
# It does NOT need to retrieve the user's original password.
# Therefore, password hashing is the correct approach.
#
# ================================================================
# 4. WHY PASSWORD HASHING MATTERS
# ================================================================
# - Reduces the damage caused by a database leak.
# - Prevents staff or developers from reading users' passwords.
# - Protects users who may reuse passwords on other websites.
# - Is a basic requirement for responsible authentication systems.
#
# IMPORTANT:
# Hashing does not make a compromised application completely safe.
# Attackers may still guess weak passwords or exploit other weaknesses.
# We also need strong password policies, secure sessions, HTTPS,
# access controls, updates and careful handling of credentials.
#
# ================================================================
# 5. HOW DJANGO HANDLES PASSWORDS
# ================================================================
# Django includes a secure password-hashing system.
#
# When we use Django's built-in user creation and password methods,
# Django handles the hashing for us.
#
# The normal flow is:
#
#     User chooses a password
#              |
#              v
#     Django receives the password
#              |
#              v
#     Django applies a password hasher
#              |
#              v
#     Django stores the encoded password hash
#              |
#              v
#     User later logs in
#              |
#              v
#     Django checks the entered password
#              |
#              v
#     Login succeeds or fails
#
# TEACH:
# Developers should not invent their own password-hashing algorithm.
# Use Django's built-in authentication and password APIs.
#
# ================================================================
# 6. STEP ONE — CHECK THE BLOG PROJECT
# ================================================================
# Our existing project is similar to:
#
#     blog/
#       manage.py
#       myproject/
#         settings.py
#         urls.py
#       myapp/
#         models.py
#         serializers.py
#         views.py
#         urls.py
#
# We will use Django's built-in User model for this lesson.
# We do not need to create a password field in the Post model.
#
# Django's authentication app is normally enabled in INSTALLED_APPS:
#
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#
# Also check that the standard authentication middleware is enabled:
#
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#
# These are normally included in a new Django project.
# Do not add duplicate entries if they are already present.
#
# ================================================================
# 7. STEP TWO — UNDERSTAND THE USER MODEL
# ================================================================
# Django provides a built-in User model for user accounts.
#
# It includes fields and methods for authentication, including:
# - username (depending on the configured user model)
# - email (depending on the project and user model)
# - password
# - is_active
# - is_staff
# - is_superuser
#
# IMPORTANT:
# The password field stores an encoded password hash, not the original
# plaintext password, when passwords are set through Django correctly.
#
# If your project uses a custom user model, use that configured model
# rather than assuming the default User model.
#
# ================================================================
# 8. STEP THREE — CREATE A USER SAFELY IN THE DJANGO SHELL
# ================================================================
# In the terminal, go to the directory containing manage.py.
#
# Start the Django shell:
#
#     python manage.py shell
#
# At the >>> prompt, enter:
#
#     from django.contrib.auth.models import User
#
# Create a test user using create_user():
#
#     user = User.objects.create_user(
#         username="student1",
#         email="student1@example.com",
#         password="ClassroomPass123!"
#     )
#
# EXPLAIN:
# create_user() creates a user and hashes the password automatically.
#
# IMPORTANT:
# This is a classroom example. Do not use a real person's password.
# Do not paste real passwords into shared terminals, screenshots,
# source code, teaching files or chat messages.
#
# If the username already exists, choose another test username or
# inspect the existing test account rather than creating duplicates.
#
# ================================================================
# 9. STEP FOUR — INSPECT WHAT DJANGO STORES
# ================================================================
# Still inside the Django shell:
#
#     user.password
#
# Explain:
# Django displays an encoded password hash, not the original password.
# It commonly contains the algorithm name, salt and derived hash data.
#
# Do not try to decode it to recover the original password.
# Password hashing is not intended to be reversed.
#
# Never print password hashes in application logs or expose them in API
# responses. Even though they are not plaintext, they are sensitive.
#
# ================================================================
# 10. STEP FIVE — VERIFY A PASSWORD WITH check_password()
# ================================================================
# In the Django shell:
#
#     user.check_password("ClassroomPass123!")
#
# Expected result:
#
#     True
#
# Try a wrong password:
#
#     user.check_password("WrongPassword")
#
# Expected result:
#
#     False
#
# EXPLAIN:
# check_password() checks the supplied password against the stored hash.
# It does not decrypt the stored hash.
#
# IMPORTANT:
# Do not compare a submitted password directly with user.password.
# user.password contains the encoded hash, not the original password.
#
# Exit the shell:
#
#     exit()
#
# ================================================================
# 11. STEP SIX — SET OR CHANGE A PASSWORD SAFELY
# ================================================================
# Django provides set_password().
#
# Example in application code:
#
#     user.set_password("AnotherStrongPass123!")
#     user.save()
#
# EXPLAIN:
# set_password() hashes the new password and updates the user object.
# save() writes the updated hash to the database.
#
# WRONG APPROACH — NEVER DO THIS:
#
#     user.password = "AnotherStrongPass123!"
#     user.save()
#
# This directly places a raw password into the password field.
# It bypasses Django's password-hashing process.
#
# CORRECT APPROACH:
#
#     user.set_password("AnotherStrongPass123!")
#     user.save()
#
# ================================================================
# 12. STEP SEVEN — AUTHENTICATE A USER
# ================================================================
# Django provides authenticate().
#
# Example:
#
#     from django.contrib.auth import authenticate
#
#     user = authenticate(
#         username="student1",
#         password="ClassroomPass123!"
#     )
#
#     if user is not None:
#         print("Login credentials are valid")
#     else:
#         print("Invalid username or password")
#
# EXPLAIN:
# authenticate() checks the supplied credentials using the configured
# authentication backends.
#
# It returns a user object when authentication succeeds, or None when
# the credentials are not accepted.
#
# In a real login view, do not print passwords or include them in logs.
# Use Django's login() function as appropriate for session-based login.
#
# ================================================================
# 13. STEP EIGHT — UNDERSTAND PASSWORD VALIDATORS
# ================================================================
# Hashing protects how passwords are stored.
# Password validators help reject weak passwords before they are saved.
#
# Open:
#     myproject/settings.py
#
# Find AUTH_PASSWORD_VALIDATORS.
# A standard Django project commonly includes validators similar to:
#
#     AUTH_PASSWORD_VALIDATORS = [
#         {
#             "NAME": (
#                 "django.contrib.auth.password_validation."
#                 "UserAttributeSimilarityValidator"
#             ),
#         },
#         {
#             "NAME": (
#                 "django.contrib.auth.password_validation."
#                 "MinimumLengthValidator"
#             ),
#             "OPTIONS": {
#                 "min_length": 10,
#             },
#         },
#         {
#             "NAME": (
#                 "django.contrib.auth.password_validation."
#                 "CommonPasswordValidator"
#             ),
#         },
#         {
#             "NAME": (
#                 "django.contrib.auth.password_validation."
#                 "NumericPasswordValidator"
#             ),
#         },
#     ]
#
# EXPLAIN EACH VALIDATOR:
#
# UserAttributeSimilarityValidator:
# Helps prevent passwords that are too similar to a user's details.
#
# MinimumLengthValidator:
# Rejects passwords shorter than the configured minimum.
#
# CommonPasswordValidator:
# Rejects passwords found in a list of commonly used passwords.
#
# NumericPasswordValidator:
# Rejects passwords made entirely of numbers.
#
# IMPORTANT:
# Validators are applied by Django forms and password-validation
# functions when those paths are used. Calling set_password() by itself
# hashes the password but does not automatically enforce every password
# validator. Validate user-chosen passwords before setting them.
#
# ================================================================
# 14. STEP NINE — VALIDATE A PASSWORD BEFORE SETTING IT
# ================================================================
# Django provides validate_password().
#
# Example for a registration or password-change flow:
#
#     from django.contrib.auth.password_validation import (
#         validate_password
#     )
#     from django.core.exceptions import ValidationError
#
#     new_password = "ClassroomPass123!"
#
#     try:
#         validate_password(new_password)
#     except ValidationError as error:
#         print(error.messages)
#     else:
#         print("Password passed validation")
#
# EXPLAIN:
# validate_password() checks the password against the validators in
# AUTH_PASSWORD_VALIDATORS.
#
# In a real registration view or serializer, return useful validation
# errors to the user. Do not expose internal details unnecessarily.
#
# ================================================================
# 15. STEP TEN — APPLY THIS TO THE BLOG REGISTRATION FEATURE
# ================================================================
# If the Blog project has a registration form, use Django's
# UserCreationForm as a safe starting point.
#
# Example file:
#     myapp/forms.py
#
#     from django import forms
#     from django.contrib.auth.forms import UserCreationForm
#     from django.contrib.auth.models import User
#
#     class BlogUserCreationForm(UserCreationForm):
#         email = forms.EmailField(required=True)
#
#         class Meta:
#             model = User
#             fields = [
#                 "username",
#                 "email",
#                 "password1",
#                 "password2",
#             ]
#
# EXPLAIN:
# UserCreationForm:
# - Provides password and password-confirmation fields.
# - Applies Django's password validation.
# - Uses Django's user-creation process, which hashes the password.
#
# NOTE:
# This example assumes the default Django User model.
# If your project uses a custom user model, adapt the form to it.
#
# ================================================================
# 16. STEP ELEVEN — NEVER STORE PASSWORDS IN YOUR BLOG POST MODEL
# ================================================================
# A Post model should store blog information such as:
# - title
# - author
# - content
# - created_at
#
# It should not store a user's login password.
#
# User credentials belong in Django's authentication system.
#
# NEVER create fields such as:
#
#     password = models.CharField(max_length=100)
#
# in a normal Blog Post model to store account passwords.
#
# Use Django's User model or a properly designed custom user model.
#
# ================================================================
# 17. SECURE CREDENTIAL STORAGE — OTHER SECRETS
# ================================================================
# Passwords are not the only sensitive values in a backend project.
#
# Examples of secrets:
# - Django SECRET_KEY
# - Database passwords
# - Email service passwords
# - API keys
# - Third-party service tokens
#
# These values must not be committed to a public Git repository.
#
# A common beginner mistake is putting secrets directly in settings.py:
#
#     SECRET_KEY = "my-real-secret-key"
#     DATABASE_PASSWORD = "my-real-database-password"
#
# Do not commit real secrets in source code.
#
# A safer approach is to load them from environment variables.
#
# Example concept in settings.py:
#
#     import os
#
#     SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
#
# For local development, a .env file can be used with a suitable
# environment-variable package, but the .env file must be ignored by Git.
#
# Example .gitignore entries:
#
#     .env
#     .env.*
#     !.env.example
#
# A committed .env.example should contain placeholders only, never
# real credentials.
#
# In production, use the hosting provider's secret/environment-variable
# settings or a dedicated secrets manager.
#
# ================================================================
# 18. SAFE HANDLING RULES TO TEACH
# ================================================================
# 1. Never store plaintext passwords.
# 2. Never invent your own password-hashing algorithm.
# 3. Use create_user(), set_password() and check_password().
# 4. Validate user-chosen passwords.
# 5. Never return password hashes from an API.
# 6. Never log passwords, tokens or secret keys.
# 7. Do not commit .env files or real secrets to Git.
# 8. Use HTTPS in production so credentials are protected in transit.
# 9. Restrict access to databases, backups and production environments.
# 10. Use secure password-reset flows; never email a user's old password.
# 11. Rotate a secret if it is accidentally exposed.
# 12. Use least-privilege database and application accounts.
#
# ================================================================
# 19. PASSWORD HASHING ALGORITHMS — SIMPLE OVERVIEW
# ================================================================
# Django supports configurable password hashers.
#
# A common default in Django projects is PBKDF2 with SHA-256.
# PBKDF2 is designed to make password guessing more expensive by
# performing repeated key-derivation work.
#
# Other password-hashing approaches include Argon2 and bcrypt.
# Django can support additional hashers when the required packages
# are installed and configured.
#
# IMPORTANT:
# - Do not use plain SHA-256 or MD5 directly for storing passwords.
# - General-purpose fast hashes make large-scale password guessing
#   easier than purpose-built password hashers.
# - Follow current Django and security guidance when selecting hashers.
# - Do not change PASSWORD_HASHERS casually in an existing project:
#   understand migration and compatibility implications first.
#
# ================================================================
# 20. PRACTICAL CLASSROOM DEMONSTRATION
# ================================================================
# Demonstration A — Create a test account:
#
#     python manage.py shell
#
#     from django.contrib.auth.models import User
#
#     user = User.objects.create_user(
#         username="blogstudent",
#         p
# assword="ClassroomPass123!"
#     )
#
# Demonstration B — Inspect the stored value:
#
#     print(user.password)
#
# Ask:
# "Can you read the original password from this value?"
#
# Expected answer:
# No. It is an encoded password hash.
#
# Demonstration C — Check the correct password:
#
#     print(user.check_password("ClassroomPass123!"))
#
# Expected:
# True
#
# Demonstration D — Check an incorrect password:
#
#     print(user.check_password("IncorrectPass"))
#
# Expected:
# False
#
# Demonstration E — Change the password safely:
#
#     user.set_password("NewClassroomPass456!")
#     user.save()
#
#     print(user.check_password("NewClassroomPass456!"))
#
# Expected:
# True
#
# Classroom safety:
# Use only disposable test accounts and invented passwords.
# Do not demonstrate with students' real passwords.
#
# ================================================================
# 21. COMMON ERRORS AND HOW TO FIX THEM
# ================================================================
# ERROR: User already exists
# CAUSE:
# The username is already in the database.
# FIX:
# Choose a different test username or inspect the existing test account.
#
# ERROR: check_password() returns False
# CHECK:
# - Did you type the exact password used to create the test account?
# - Did you change the password after creating the account?
# - Are you checking the correct user object?
#
# ERROR: Password is stored as readable text
# CAUSE:
# Code may have assigned directly to user.password.
# FIX:
# Use set_password() and save the user.
# If a real plaintext password was stored, treat it as exposed:
# reset it securely and investigate any affected accounts.
#
# ERROR: Password validators do not seem to run
# CHECK:
# - Are AUTH_PASSWORD_VALIDATORS configured?
# - Does the registration or password-change flow call validation?
# - Remember: set_password() hashes but does not itself enforce all
#   configured validators.
#
# ERROR: SECRET_KEY is None
# CAUSE:
# The environment variable is not set.
# FIX:
# Set DJANGO_SECRET_KEY in the local environment or hosting settings.
# Do not solve this by committing a real production secret.
#
# ================================================================
# 22. PRACTICAL STUDENT EXERCISE
# ================================================================
# Ask students to complete these tasks:
#
# 1. Open the existing Django Blog project.
# 2. Start the Django shell.
# 3. Create a test user with create_user().
# 4. Inspect the user's password field.
# 5. Explain why it is not the original password.
# 6. Verify the correct password with check_password().
# 7. Verify an incorrect password.
# 8. Change the password with set_password().
# 9. Verify the new password.
# 10. Find AUTH_PASSWORD_VALIDATORS in settings.py.
# 11. Explain the purpose of two validators.
# 12. Find where the project's SECRET_KEY is configured.
# 13. Explain why real secrets should not be committed to Git.
#
# ================================================================
# 23. REVISION SUMMARY
# ================================================================
# Password hashing:
# Converts a password into a one-way encoded value for secure storage.
#
# Plaintext password:
# The original readable password. Do not store it.
#
# Password hash:
# The encoded value Django stores and checks during authentication.
#
# create_user():
# Creates a user and hashes the supplied password.
#
# set_password():
# Safely sets or changes a user's password hash.
#
# check_password():
# Checks whether a supplied password matches the stored hash.
#
# authenticate():
# Checks credentials using Django's configured authentication system.
#
# validate_password():
# Applies the configured password validators.
#
# Environment variable:
# A way to provide configuration and secrets without hardcoding them
# into committed source code.
#
# REMEMBER:
#     Never store plaintext passwords.
#     Let Django handle password hashing.
#     Keep secrets out of Git.
#
# ================================================================
# 24. OBJECTIVE QUESTIONS — CHOOSE THE BEST ANSWER
# ================================================================
#
# Q1. What should an application store for a user's password?
# A. Plaintext password
# B. Password hash
# C. Password in a blog post
# D. Password in a log file
#
# Q2. Is password hashing designed to be reversed?
# A. Yes, with a username
# B. Yes, with a database query
# C. No, it is designed as a one-way process
# D. Yes, with HTML
#
# Q3. What is the main difference between hashing and encryption?
# A. They are exactly the same
# B. Encryption is reversible with a key; password hashing is one-way
# C. Hashing is used only for images
# D. Encryption cannot protect data
#
# Q4. Which Django method creates a user and hashes the password?
# A. create_user()
# B. create_post()
# C. save_plaintext()
# D. render()
#
# Q5. Which method safely sets a user's password?
# A. set_password()
# B. set_title()
# C. password_text()
# D. create_url()
#
# Q6. Which method checks whether a password matches the stored hash?
# A. password_matches_database()
# B. check_password()
# C. decrypt_password()
# D. get_password_text()
#
# Q7. What does authenticate() do?
# A. Creates a blog post
# B. Checks credentials using Django authentication backends
# C. Displays a CSS file
# D. Deletes the database
#
# Q8. What does validate_password() do?
# A. Encrypts the database
# B. Checks a password against configured validators
# C. Creates a JWT automatically
# D. Changes a username
#
# Q9. Does set_password() by itself enforce every configured password
# validator?
# A. Yes, always
# B. No, validation must be applied separately
# C. Only on Fridays
# D. Only when using SQLite
#
# Q10. Which is the unsafe way to change a password?
# A. user.set_password("NewPassword123!")
# B. user.password = "NewPassword123!"
# C. user.save() after set_password()
# D. Using Django's password forms
#
# Q11. Where should a Django SECRET_KEY be kept in production?
# A. In a public GitHub repository
# B. In a public blog post
# C. In secure environment configuration or a secrets manager
# D. In a student's password field
#
# Q12. Should password hashes be returned in an API response?
# A. Yes, for convenience
# B. No, they are sensitive credential data
# C. Yes, if the user asks
# D. Only in HTML
#
# Q13. What is the purpose of CommonPasswordValidator?
# A. Reject commonly used passwords
# B. Create database backups
# C. Hash blog titles
# D. Generate URL routes
#
# Q14. Which is a safer way to protect credentials while they travel
# between a browser and a production website?
# A. HTTP only
# B. HTTPS
# C. A public text file
# D. A screenshot
#
# Q15. Should developers create their own password-hashing algorithm?
# A. Yes, for every project
# B. No, use established framework password-hashing tools
# C. Yes, using MD5 directly
# D. Only for blog applications
#
# Q16. What does a password hash normally allow the application to do?
# A. Recover the original password
# B. Verify a password attempt
# C. Display the password to staff
# D. Send the password by email
#
# Q17. Which model should normally manage login credentials in a Django
# application?
# A. The Blog Post model
# B. Django's configured user model
# C. The Comment model
# D. The Category model
#
# Q18. What should you do if a real secret is accidentally committed?
# A. Ignore it
# B. Rotate/revoke the exposed secret and investigate
# C. Rename the file only
# D. Make the repository public
#
# Q19. What is a password validator used for?
# A. To help reject weak or unsuitable passwords
# B. To create blog categories
# C. To format HTML
# D. To connect a router
#
# Q20. Which statement is correct?
# A. Hashing alone makes an entire application secure
# B. Password hashes should be logged
# C. Secure credential storage is one part of a wider security strategy
# D. Passwords should be stored in plaintext for recovery
#
# ================================================================
# 25. ANSWER KEY
# ================================================================
# Q1: B
# Q2: C
# Q3: B
# Q4: A
# Q5: A
# Q6: B
# Q7: B
# Q8: B
# Q9: B
# Q10: B
# Q11: C
# Q12: B
# Q13: A
# Q14: B
# Q15: B
# Q16: B
# Q17: B
# Q18: B
# Q19: A
# Q20: C
#
# END OF GUIDE
