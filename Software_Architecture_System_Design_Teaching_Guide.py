"""
SOFTWARE ARCHITECTURE & SYSTEM DESIGN
MONOLITH VS MICROSERVICES | SCALABILITY
============================================================

LEARNING OBJECTIVES
By the end of this lesson, students should be able to:
1. Explain software architecture and system design.
2. Describe monolithic and microservices architectures.
3. Compare their benefits and limitations.
4. Explain scalability, vertical scaling and horizontal scaling.
5. Explain the role of a load balancer.
6. Recommend an architecture for a project and justify the choice.

TEACHING METHOD
Use the existing Django Blog project throughout this lesson. Start with
simple explanations and diagrams, then demonstrate how Django apps can
be organised inside one application. This is mainly a design lesson;
students do not need to convert their blog into microservices.

============================================================
1. INTRODUCE SOFTWARE ARCHITECTURE
============================================================

ASK THE CLASS:
"If you were asked to build a school portal, what would you plan before
writing code?"

Possible answers:
- What the system should do.
- Who will use it.
- What information it stores.
- How users log in.
- How the different parts communicate.
- How it will handle many users.

SIMPLE EXPLANATION:
Software architecture is the high-level structure of an application. It
describes the main parts of a system and how those parts work together.

System design is planning how the system will work:
- What components are required?
- What is each component responsible for?
- How will components communicate?
- Where will data be stored?
- How will the system handle growth and failures?

ANALOGY:
An architect plans a building before construction. A software developer
plans the structure of an application before building a large system.

TEACHING CHECK:
Ask: "Does system design mean writing Python code?"
Expected answer: No. It is mainly about planning the system's structure
and behaviour before or during implementation.

============================================================
2. CONNECT THE TOPIC TO OUR DJANGO BLOG
============================================================

Open the existing Django Blog project. Ask students to identify:
- Browser: where the user views the blog.
- URLs: direct requests to the correct view.
- Views: receive requests and decide what happens.
- Models: describe the data.
- Database: stores posts and user information.
- Templates: display HTML pages.

Draw this request flow:

USER / BROWSER
      |
      v
DJANGO URLS
      |
      v
DJANGO VIEWS
      |
      v
MODELS / BUSINESS LOGIC
      |
      v
DATABASE
      |
      v
RESPONSE TO USER

EXPLAIN STEP BY STEP:
1. A user opens a blog post.
2. The browser sends a request.
3. Django checks the URL pattern.
4. The matching view runs.
5. The view retrieves the post from the database.
6. Django returns a response to the browser.

ASK: "What happens when a user clicks on a blog post?"
Let students explain the flow in their own words.

============================================================
3. MONOLITHIC ARCHITECTURE
============================================================

SIMPLE EXPLANATION:
A monolithic application is built and deployed as one main application.
It may contain many modules or Django apps, but the application is
commonly released as one unit.

DJANGO BLOG EXAMPLE:
- User accounts
- Blog posts
- Comments
- Categories
- Search
- Admin features

DIAGRAM:

          DJANGO BLOG APPLICATION
    +--------------------------------+
    |          User Accounts         |
    |--------------------------------|
    |          Blog Posts            |
    |--------------------------------|
    |          Comments              |
    |--------------------------------|
    |          Categories            |
    |--------------------------------|
    |          Search                |
    +--------------------------------+
                    |
                    v
                DATABASE

WHY MONOLITHS ARE USEFUL:
- Easier to start with.
- Usually simpler to develop and deploy.
- Easier for a small team to manage.
- Components can communicate directly inside the application.
- Requires less infrastructure at the beginning.

POSSIBLE DISADVANTAGES:
- A large, poorly organised codebase can become difficult to maintain.
- A change in one area may affect another area.
- The whole application is commonly deployed together.
- Scaling only one feature independently is more difficult.

STEP-BY-STEP DJANGO DEMONSTRATION:
1. Open the Django Blog folder.
2. Show manage.py and the project folder.
3. Open the app containing the Post model.
4. Show models.py, views.py, urls.py and templates.
5. Explain that these files have different responsibilities.
6. Explain that the project can still be a monolith when deployed
   together as one application.

IMPORTANT:
A monolith does NOT mean all code must be inside one file. A Django
project can contain multiple apps and still be a monolith.

QUICK EXERCISE:
Ask: "If our Django project has five Django apps, does that automatically
mean it uses microservices?"
Expected answer: No. Django apps are code organisation units. They are
not automatically independently deployed services.

============================================================
4. MICROSERVICES ARCHITECTURE
============================================================

SIMPLE EXPLANATION:
Microservices architecture divides a system into smaller, independent
services. Each service is responsible for a particular business function.

ONLINE STORE EXAMPLE:
- User Service: manages customer accounts.
- Product Service: manages products.
- Order Service: manages orders.
- Payment Service: handles payments.
- Notification Service: sends messages.

DIAGRAM:

                ONLINE STORE
                     |
       +-------------+-------------+
       |             |             |
       v             v             v
  USER SERVICE  PRODUCT SERVICE  ORDER SERVICE
       |             |             |
       v             v             v
   USER DATA     PRODUCT DATA    ORDER DATA
                     |
                     v
               PAYMENT SERVICE
                     |
                     v
                 PAYMENT DATA

EXPLAIN:
Each service has its own responsibility. Services commonly communicate
through APIs or messaging systems.

POSSIBLE BENEFITS:
- Services can be deployed independently.
- A busy service can be scaled separately.
- Different teams can own different services.
- A failure may be isolated if the system is designed correctly.
- A service can use a suitable technology where there is a real need.

POSSIBLE DISADVANTAGES:
- More difficult to build and operate.
- Services communicate over a network.
- Network failures and timeouts must be handled.
- Debugging across services is harder.
- Data consistency can be more complicated.
- Monitoring and deployment require more work.

STEP-BY-STEP TEACHING DEMONSTRATION:
1. Draw the online store services on the board.
2. Explain the responsibility of each service.
3. Ask what happens if the payment service becomes unavailable.
4. Explain that the order service must handle the failure safely.
5. Explain that services communicate through APIs or messages.

QUICK EXERCISE:
Ask students to name three possible services in an ecommerce platform.
Possible answers: user, product, order, payment, delivery, notification.

============================================================
5. MONOLITH VS MICROSERVICES
============================================================

MONOLITH:
- One main application.
- Commonly deployed as one unit.
- Usually simpler to begin with.
- Internal components can communicate directly.
- Scaling often means scaling the application as a whole.
- Suitable for many small and medium projects.

MICROSERVICES:
- Several independent services.
- Services can be deployed separately.
- More infrastructure and coordination are needed.
- Services communicate through APIs or messages.
- Individual services can be scaled independently.
- Useful when the system and organisation justify the complexity.

CLASS DISCUSSION:
SCENARIO A: One developer is building a personal blog with login, posts
and comments. Recommended starting point: a well-organised monolith.

SCENARIO B: A large online store has separate teams for payments, orders,
delivery and products. Each area has different traffic and release needs.
Microservices may be useful if independent ownership, deployment and
scaling justify the extra complexity.

KEY MESSAGE:
Microservices are not automatically better. Choose based on requirements,
team size, skills, budget, expected traffic and operational capacity.

============================================================
6. SCALABILITY
============================================================

SIMPLE EXPLANATION:
Scalability is the ability of a system to handle an increase in workload
without becoming unacceptably slow or unreliable.

EXAMPLE:
A blog normally receives 20 visitors each day. A popular post is shared
and suddenly 5,000 people visit. Can the application handle the increase?

Workload may increase through more users, requests, database records,
file uploads and background tasks.

A. VERTICAL SCALING
Vertical scaling means increasing the resources of one server.
Examples: more RAM, more CPU power or faster storage.

       BEFORE                 AFTER
   +-----------+          +-------------+
   |  SERVER   |          |   SERVER    |
   |  2 CPU    |   --->   |   8 CPU     |
   |  4 GB RAM |          |  32 GB RAM  |
   +-----------+          +-------------+

Advantages:
- Simple to understand.
- May need fewer application changes.
- Can be a practical first step.

Limitations:
- A server has hardware limits.
- Powerful machines can become expensive.
- One machine may remain a single point of failure.

B. HORIZONTAL SCALING
Horizontal scaling means adding more servers or application instances.

             LOAD BALANCER
             /     |     \\
            v      v      v
         SERVER  SERVER  SERVER
            |      |      |
            +------+------+
                   |
                DATABASE

Advantages:
- More instances can handle more requests.
- Can improve availability when designed correctly.
- Capacity can grow by adding instances.

Limitations:
- More infrastructure is required.
- A load balancer may be needed.
- Sessions, files and shared data need careful handling.
- More servers do not automatically solve database bottlenecks.

CHECK UNDERSTANDING:
1. Upgrade a server from 4 GB RAM to 16 GB RAM. Answer: Vertical.
2. Add three more application servers. Answer: Horizontal.

============================================================
7. LOAD BALANCER
============================================================

SIMPLE EXPLANATION:
A load balancer distributes incoming requests across multiple servers.

                  USERS
                    |
                    v
              LOAD BALANCER
               /    |    \\
              v     v     v
           SERVER SERVER SERVER

Explain: Instead of sending every request to one server, the load
balancer distributes work across available servers.

ASK: "What could happen if one server receives all requests while the
others are idle?"
Expected answer: The first server may become overloaded.

============================================================
8. SCALABILITY IS NOT ONLY ABOUT SERVERS
============================================================

An application may be slow because of:
- Inefficient database queries.
- Missing database indexes.
- Large images and files.
- Slow external APIs.
- Too much work inside a request.
- Poor caching.
- Limited server resources.

CONNECT TO DJANGO:
- Pagination reduces the number of records returned at once.
- Database indexes can improve selected queries.
- Caching reduces repeated work.
- Background jobs can move slow tasks outside the request-response cycle.
- Efficient queries reduce unnecessary database work.

Do not teach all these techniques in depth here. Explain that they are
additional tools for improving application performance.

ASK: "Will adding more servers always make a slow application fast?"
Expected answer: No. The database, code, network or another dependency
may be the real bottleneck.

============================================================
9. PRACTICAL DJANGO STRUCTURE DEMONSTRATION
============================================================

Show how a monolithic Django project can still be organised into apps.

ILLUSTRATIVE STRUCTURE:

blog/
    manage.py
    blog/
        settings.py
        urls.py
    posts/
        models.py
        views.py
        urls.py
    accounts/
        models.py
        views.py
        urls.py
    comments/
        models.py
        views.py
        urls.py

Explain:
- posts handles blog posts.
- accounts handles user accounts.
- comments handles comments.
- The main project connects their URL configurations.
- If all are deployed together as one application, this can still be
  a monolith.

OPTIONAL CODE EXAMPLE:

# blog/urls.py
from django.urls import path, include

urlpatterns = [
    path("posts/", include("posts.urls")),
    path("accounts/", include("accounts.urls")),
    path("comments/", include("comments.urls")),
]

Explain:
1. include connects another URL configuration.
2. Each app can manage its own URLs.
3. The main project connects the apps.
4. This improves organisation.
5. It does not automatically create microservices.

This is illustrative. Do not rename or move existing project files unless
you are deliberately teaching Django app organisation.

============================================================
10. OPTIONAL API COMMUNICATION EXAMPLE
============================================================

Explain that independent services commonly communicate through HTTP APIs.
This example only works if a service exists at the example address.

# Install requests in the active virtual environment if needed:
# pip install requests
import requests

url = "http://localhost:8001/api/products/"

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    products = response.json()
    print(products)
except requests.RequestException as error:
    print("Could not contact the product service:", error)

Explain:
- The client sends an HTTP request.
- The service receives the request.
- The service returns data, often JSON.
- Network requests can fail, so timeouts and error handling matter.

============================================================
11. COMMON MISUNDERSTANDINGS
============================================================

1. "Every Django app is a microservice."
   Correction: A Django app is a code organisation unit.
2. "Microservices are always better."
   Correction: They add complexity and should solve a real problem.
3. "A monolith puts all code in one file."
   Correction: A monolith can contain many modules and apps.
4. "Scalability only means adding servers."
   Correction: Scaling can also involve better hardware, efficient code,
   database improvements and caching.
5. "More servers always make an application reliable."
   Correction: Reliability also requires monitoring, health checks,
   failure handling and careful data management.

============================================================
12. CLASSROOM RECAP
============================================================

Ask students to complete:
1. Software architecture is the __________ of an application.
   Expected: high-level structure.
2. A monolith is commonly deployed as __________.
   Expected: one main application/unit.
3. Microservices divide a system into __________.
   Expected: smaller independent services.
4. Vertical scaling increases the resources of __________.
   Expected: one server/machine.
5. Horizontal scaling adds __________.
   Expected: more servers/instances.
6. A load balancer distributes __________.
   Expected: incoming requests/traffic.
7. Architecture should be selected based on __________.
   Expected: project requirements and constraints.

============================================================
13. STUDENT PRACTICAL EXERCISES
============================================================

EXERCISE 1: DRAW A MONOLITH
Draw a school portal containing login, student records, attendance,
results and announcements. Show these features inside one application.

EXERCISE 2: DRAW MICROSERVICES
Redraw the school portal as separate services. Show at least three
services and how they communicate.

EXERCISE 3: COMPARE
Write five differences between monolithic and microservices architecture.

EXERCISE 4: IDENTIFY THE SCALING METHOD
A. Upgrade a server from 8 GB RAM to 32 GB RAM.
B. Add two more application servers.
C. Move an application to a machine with more CPU cores.
D. Run four application instances behind a load balancer.

EXERCISE 5: MAKE A DESIGN DECISION
A small team is building a blog for a school. Recommend an architecture
and give three reasons.

EXERCISE 6: TRACE THE DJANGO BLOG
Identify the project URL file, app URL file, views, models and database.
Explain how a request moves through the application.

============================================================
14. OBJECTIVE QUESTIONS
============================================================

Choose the correct answer.

1. What is software architecture?
A. A programming language
B. The high-level structure of an application
C. A database table
D. A CSS framework

2. System design is mainly concerned with:
A. Choosing font colours
B. Planning how system components work together
C. Writing only HTML
D. Installing a code editor

3. A monolithic application is commonly:
A. Deployed as one main application
B. Made only of HTML
C. Required to use many databases
D. Unable to use modules

4. Which statement about a monolith is correct?
A. All code must be in one file
B. It cannot contain separate Django apps
C. It can contain multiple modules and apps
D. It must use microservices

5. What is a microservice?
A. A small computer
B. An independent service responsible for a capability
C. A CSS component
D. A Python comment

6. How do microservices commonly communicate?
A. Through APIs or messaging
B. Only through CSS
C. Only through keyboard input
D. Through HTML headings

7. Which is a possible benefit of microservices?
A. No network failures
B. Independent deployment of services
C. No monitoring required
D. No testing required

8. Which is a possible disadvantage of microservices?
A. They cannot use APIs
B. They must use one file
C. Increased operational complexity
D. They cannot be deployed

9. A sensible starting point for a small blog is often:
A. Microservices in every case
B. A well-organised monolith
C. No architecture
D. A server for every page

10. Scalability means:
A. Changing website colours
B. Handling increased workload effectively
C. Deleting database records
D. Removing user accounts

11. Vertical scaling means:
A. Adding more servers
B. Increasing the resources of one server
C. Creating more URLs
D. Splitting a database table

12. Horizontal scaling means:
A. Adding more servers or instances
B. Increasing one server's RAM only
C. Changing a password
D. Removing the load balancer

13. What does a load balancer do?
A. Writes migrations
B. Distributes requests across servers
C. Designs web pages
D. Hashes passwords

14. Does adding more servers always solve poor performance?
A. Yes, always
B. No, the bottleneck may be elsewhere
C. Only with SQLite
D. Only with HTML

15. A Django project with several apps deployed together can still be:
A. A monolith
B. A load balancer
C. A database index
D. A network protocol

16. Which factors influence architecture decisions?
A. Project requirements
B. Team skills
C. Budget and expected traffic
D. All of the above

17. Which could be a microservice in an online store?
A. Payment service
B. Bold text service
C. Keyboard service
D. Wallpaper service

18. A poorly organised monolith may become:
A. Unable to store data
B. Difficult to maintain
C. Unable to use Python
D. Unable to have URLs

19. Which statement is correct?
A. Microservices are always best
B. Monoliths cannot scale
C. Architecture should fit the project's needs
D. Every student project needs Kubernetes

20. What should developers do before choosing an architecture?
A. Copy the latest trend
B. Understand requirements and constraints
C. Ignore team size
D. Avoid planning

============================================================
15. OBJECTIVE ANSWER KEY
============================================================

1. B   2. B   3. A   4. C   5. B
6. A   7. B   8. C   9. B   10. B
11. B  12. A  13. B  14. B  15. A
16. D  17. A  18. B  19. C  20. B

============================================================
16. HOMEWORK
============================================================

TITLE: DESIGN THE ARCHITECTURE OF A SCHOOL PORTAL

A school wants an application containing student registration, login,
attendance, examination results and announcements.

Students should submit:
1. A short explanation of the system's purpose.
2. A diagram showing a monolithic design.
3. A diagram showing a possible microservices design.
4. Three advantages and three disadvantages of each approach.
5. A recommendation with reasons.
6. An explanation of how the system could scale if student numbers grow.

Use clear labels and explain the reasoning. Do not choose microservices
only because they sound more advanced.

============================================================
17. FINAL MESSAGE TO STUDENTS
============================================================

There is no single architecture that is best for every application.
A good developer understands the problem, considers the team's ability,
budget, expected workload and future needs, and then chooses a suitable
design.

Start simple. Keep code organised. Measure real problems. Introduce more
complex architecture only when there is a clear reason.

KEY TAKEAWAY:
A well-designed monolith is often better than poorly designed microservices.
"""
