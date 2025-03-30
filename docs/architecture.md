# Overview

The Task Management System is a web-based application designed to help users organize and manage their tasks efficiently. Whether you’re an individual tracking personal to-dos or part of a small team coordinating responsibilities, this system provides a simple, secure, and scalable solution. Users can sign up, log in, create tasks, view their task list, update task details, delete tasks, and recover their account if they forget their password—all through an intuitive interface accessible from any modern web browser.

The system leverages a serverless architecture on Amazon Web Services (AWS), meaning there are no traditional servers to manage. Instead, it uses cloud services that automatically scale with demand, reduce costs, and simplify maintenance. This document dives deep into every aspect of the system, from its purpose and features to the technical details of its backend, frontend, database, and security measures.

## Project Purpose

The Task Management System exists to solve a common problem: keeping track of tasks in an organized, accessible, and secure way. Its primary goals are to:

- **Enable account creation**: Allow users to sign up with an email and password, verified through a one-time password (OTP) sent to their inbox.
- **Secure access**: Provide a login/logout system so users can access their personal task data safely.
- **Simplify task management**: Let users create, view, update, and delete tasks with ease, including details like descriptions, due dates, and statuses (e.g., "pending" or "completed").
- **Support account recovery**: Offer a password reset option using OTPs to ensure users can regain access if they forget their credentials.

The system is designed to be user-friendly (easy to navigate), secure (protecting user data), and scalable (able to grow with the number of users), making it ideal for personal use or small collaborative teams.

## Key Features

Here’s what the Task Management System offers, broken down into its core functionalities:

### 1. User Authentication

- **Signup**: New users can create an account by entering a unique username, email, and password. To confirm their identity, they receive an OTP via email, which they must enter to complete registration.
- **Login**: Existing users log in with their username and password. Upon success, they receive a secure token (a JSON Web Token, or JWT) stored in a browser cookie, allowing them to access their tasks.
- **Logout**: Users can log out, which clears the token from their browser, ending their session.
- **Forgot Password**: If users forget their password, they can request a reset by entering their email. An OTP is sent to verify their identity, after which they can set a new password.

### 2. Task Management (CRUD Operations)

- **Create Task**: Users can add a new task by specifying a description (e.g., "Finish report"), a due date (e.g., "2023-12-15"), and a status (e.g., "pending").
- **Read Tasks**: Users can view a list of all their tasks, showing details like descriptions, due dates, and statuses.
- **Update Task**: Users can edit an existing task’s description, due date, or status (e.g., change "pending" to "completed").
- **Delete Task**: Users can remove tasks they no longer need, keeping their list clean and relevant.

### 3. Security

- Passwords are encrypted (hashed) using a strong algorithm (e.g., bcrypt) before storage, ensuring they remain safe even if the database is compromised.
- JWTs are stored in HTTP-only cookies, making them inaccessible to malicious scripts and protecting against theft.
- OTPs provide an additional layer of verification for signup and password resets, ensuring only legitimate users gain access.

### 4. Scalability and Cost Efficiency

- The system uses AWS Lambda, which automatically adjusts computing power based on the number of users, so it works seamlessly whether there are 10 users or 10,000.
- The database (Aurora PostgreSQL Serverless) scales up or down as needed and pauses when idle, keeping costs low during quiet periods.

## Technology Stack

The Task Management System is built using modern tools and services that balance simplicity, performance, and scalability. Here’s the breakdown:

### Backend

- **AWS Lambda**: A serverless compute service that runs the backend code whenever an action (like logging in or creating a task) is triggered. It eliminates the need for managing servers.
- **Amazon API Gateway**: Acts as a "front door" for the backend, handling incoming requests (e.g., from the web app) and directing them to the right Lambda function.
- **Amazon Aurora PostgreSQL Serverless**: A relational database that stores user accounts and tasks. It’s serverless, meaning it scales automatically and requires minimal upkeep.
- **Amazon SES (Simple Email Service)**: Sends emails, such as OTPs, to users during signup and password recovery.
- **Python**: The programming language used to write the backend logic in Lambda functions. It’s chosen for its readability and strong AWS support.

### Frontend

- **React.js**: A JavaScript framework that builds the interactive, single-page web application (SPA) users see and interact with.
- **Axios (or Fetch API)**: A tool for sending requests (e.g., "get my tasks") from the frontend to the backend.
- **CSS (or Tailwind CSS)**: Styles the interface to make it visually appealing and easy to use.

### Additional Tools

- **AWS SAM (Serverless Application Model)**: Helps developers test the backend locally before deploying it to AWS.
- **Docker**: Runs a local version of the PostgreSQL database during development.
- **Git**: Tracks changes to the code, allowing multiple developers to collaborate effectively.

## Architecture Overview

The Task Management System uses a client-server architecture, where the frontend (the client) communicates with the backend (the server) over the internet using RESTful APIs (a standard way of exchanging data). The backend is serverless, relying on AWS services to handle requests and store data.

### High-Level Architecture Diagram

```
[Frontend: React SPA] <--> [Amazon API Gateway] <--> [AWS Lambda Functions] <--> [Amazon Aurora PostgreSQL]
                                                                |
                                                                v
                                                        [Amazon SES (Emails)]
```

- **Frontend**: The web app users see in their browser. It’s built as a single-page application (SPA), meaning it loads once and updates dynamically without full page reloads.
- **Amazon API Gateway**: Receives requests from the frontend (e.g., "log me in" or "create a task") and routes them to the appropriate Lambda function.
- **AWS Lambda Functions**: Small pieces of code that run in response to requests. Each function handles a specific task, like verifying a login or saving a new task to the database.
- **Amazon Aurora PostgreSQL**: The database where user accounts and tasks are stored. It’s relational, meaning data is organized in tables with clear relationships (e.g., tasks linked to users).
- **Amazon SES**: Sends emails for OTPs when users sign up or reset their password.

## Backend Architecture

The backend is the engine of the system, handling all the logic behind user actions. It’s built as a collection of Lambda functions, supported by utility modules and tests, and connected to a database.

### Folder Structure

```
backend/
├── handlers/
│   ├── auth/
│   │   ├── login.py         # Handles user login
│   │   ├── signup.py        # Registers new users
│   │   ├── logout.py        # Clears user session (client-side)
│   │   ├── forgot_password.py  # Starts password reset process
│   │   ├── reset_password.py   # Completes password reset
│   │   └── verify_otp.py    # Verifies OTPs
│   └── tasks/
│       ├── create_task.py   # Adds a new task
│       ├── get_tasks.py     # Fetches a user’s tasks
│       ├── update_task.py   # Edits a task
│       └── delete_task.py   # Removes a task
├── utils/
│   ├── db.py               # Connects to the database
│   ├── auth.py             # Manages JWTs
│   ├── email.py            # Sends emails via SES
│   └── validators.py       # Checks user inputs
├── tests/
│   ├── test_login.py       # Tests login functionality
│   ├── test_signup.py      # Tests signup functionality
│   └── ... (other tests)
├── requirements.txt         # Lists Python dependencies
└── template.yaml            # Defines AWS resources
```

### Key Components

- **Handlers (handlers/)**: Individual Lambda functions that process specific actions.
  - **Auth Handlers (auth/)**: Manage user authentication.
    - login.py: Checks username/password, issues a JWT if correct.
    - signup.py: Creates a new user account and sends an OTP.
    - logout.py: Instructs the frontend to clear the JWT cookie.
    - forgot_password.py: Sends an OTP for password recovery.
    - reset_password.py: Updates the password after OTP verification.
    - verify_otp.py: Confirms the OTP entered by the user.
  - **Task Handlers (tasks/)**: Manage task operations.
    - create_task.py: Saves a new task to the database.
    - get_tasks.py: Retrieves all tasks for the logged-in user.
    - update_task.py: Updates a task’s details.
    - delete_task.py: Deletes a task from the database.
- **Utilities (utils/)**: Shared code used by multiple handlers.
  - db.py: Opens connections to Aurora PostgreSQL and runs SQL queries (e.g., "SELECT * FROM tasks").
  - auth.py: Creates and validates JWTs for secure sessions.
  - email.py: Uses Amazon SES to send OTP emails.
  - validators.py: Ensures inputs (e.g., email addresses) are valid and safe.
- **Tests (tests/)**: Automated checks to verify each handler works correctly.
  - Example: test_login.py tests various login scenarios (correct credentials, wrong password, etc.).
- **Configuration Files**:
  - requirements.txt: Lists Python libraries (e.g., boto3 for AWS, pyjwt for tokens).
  - template.yaml: An AWS SAM file defining Lambda functions, API Gateway, and other resources.

## Database Schema

The system uses Amazon Aurora PostgreSQL Serverless to store data in two tables:

- **Users Table**: Holds user account details.
  - user_id (Unique ID for each user, e.g., 1, 2, 3)
  - username (Unique, e.g., "john_doe")
  - email (Unique, e.g., "john@example.com")
  - password_hash (Encrypted password)
  - reset_token (Temporary code for password resets)
  - reset_expires_at (When the reset token expires)
  - created_at (Signup timestamp)
  - updated_at (Last update timestamp)
- **Tasks Table**: Stores tasks linked to users.
  - task_id (Unique ID for each task)
  - user_id (Links to users.user_id, e.g., 1)
  - description (e.g., "Buy groceries")
  - due_date (e.g., "2023-12-10")
  - status (e.g., "pending" or "completed")
  - created_at (Task creation timestamp)
  - updated_at (Last update timestamp)

The user_id in the Tasks table connects each task to its owner, ensuring users only see their own tasks.

## Authentication Flow

- **Login**:
  - User enters username and password in the frontend.
  - login.py checks the credentials against the database.
  - If valid, it generates a JWT and sends it to the frontend in an HTTP-only cookie.
  - The user is redirected to their task list.
- **Logout**:
  - User clicks "Logout" in the frontend.
  - The JWT cookie is cleared from the browser (no backend action needed).
- **Signup**:
  - User submits username, email, and password.
  - signup.py validates the data, stores the user with a hashed password, and sends an OTP email.
  - User enters the OTP, and verify_otp.py activates the account.
- **Forgot Password**:
  - User enters their email in the "Forgot Password" form.
  - forgot_password.py sends an OTP to the email.
  - User enters the OTP, and reset_password.py updates the password after verification.

## Frontend Architecture

The frontend is a single-page application (SPA) built with React.js, offering a smooth, responsive experience. It talks to the backend via API calls.

### Folder Structure

```
frontend/
├── public/
│   ├── index.html          # Base HTML file
│   └── ... (images, etc.)
├── src/
│   ├── components/
│   │   ├── auth/
│   │   │   ├── Login.js    # Login form
│   │   │   ├── Signup.js   # Signup form
│   │   │   ├── ForgotPassword.js  # Password reset form
│   │   │   └── ... (other auth UI)
│   │   └── tasks/
│   │       ├── TaskList.js  # Displays tasks
│   │       ├── CreateTask.js  # New task form
│   │       ├── UpdateTask.js  # Edit task form
│   │       └── ... (other task UI)
│   ├── pages/
│   │   ├── Home.js         # Main dashboard
│   │   ├── LoginPage.js    # Login page
│   │   ├── SignupPage.js   # Signup page
│   │   └── ... (other pages)
│   ├── services/
│   │   ├── api.js          # API request handler
│   │   └── auth.js         # Authentication logic
│   ├── App.js              # Main app component
│   ├── index.js            # Entry point
│   └── ... (styles, etc.)
├── .env                    # Environment variables
└── package.json            # Dependencies and scripts
```

### Key Components

- **Components (src/components/)**: Reusable UI pieces.
  - **Auth Components (auth/)**:
    - Login.js: Form for entering username/password.
    - Signup.js: Form for new user registration.
    - ForgotPassword.js: Form for password recovery.
  - **Task Components (tasks/)**:
    - TaskList.js: Shows all tasks in a table or list.
    - CreateTask.js: Form to add a new task.
    - UpdateTask.js: Form to modify a task.
- **Pages (src/pages/)**: Full-screen views for different routes.
  - Home.js: Displays the task list for logged-in users.
  - LoginPage.js: Shows the login form.
  - SignupPage.js: Shows the signup form.
- **Services (src/services/)**:
  - api.js: Sends requests to the backend (e.g., "POST /tasks" to create a task).
  - auth.js: Manages login state and JWT handling.
- **Configuration Files**:
  - .env: Stores settings like the API URL (e.g., https://api.example.com).
  - package.json: Lists dependencies (e.g., React, Axios) and commands (e.g., npm start).

## User Interface Flow

- **Unauthenticated User**:
  - Starts at the login or signup page.
  - After successful login/signup, redirected to the homepage.
- **Authenticated User**:
  - Homepage shows their task list.
  - Can add, edit, or delete tasks via buttons and forms.
  - Logs out to return to the login page.

## How the System Works Together

Here’s how a user action flows through the system:

1. **User Action**:
   - The user clicks "Login" and submits their credentials.
   - The frontend sends a POST request to /login with the username and password.
2. **API Gateway**:
   - Receives the /login request and forwards it to the login.py Lambda function.
3. **Lambda Function**:
   - login.py queries the database to verify the credentials.
   - If correct, it generates a JWT and returns it in an HTTP-only cookie.
   - If incorrect, it returns an error message.
4. **Database**:
   - Provides the stored password hash for login.py to compare against.
5. **Frontend Response**:
   - API Gateway sends the response (JWT or error) back to the frontend.
   - The frontend stores the JWT cookie and redirects the user to their task list, or shows an error if login fails.

This flow repeats for other actions (e.g., creating a task), with different endpoints and Lambda functions handling each request.

## Security Considerations

- **Password Hashing**: Passwords are hashed with bcrypt, making them unreadable even if the database is accessed.
- **JWT Security**: Stored in HTTP-only cookies, safe from JavaScript-based attacks (XSS).
- **OTP Protection**: Adds a second verification step for signup and password resets.
- **Input Validation**: Both frontend and backend check inputs to block attacks like SQL injection or XSS.

## Scalability and Performance

- **Serverless Scaling**: AWS Lambda and Aurora PostgreSQL adjust resources automatically as user demand grows or shrinks.
- **Caching**: API Gateway can cache responses (e.g., task lists) to speed up frequent requests.
- **Cost Efficiency**: You only pay for what you use—no idle servers mean lower costs.

## Local Development and Testing

- **AWS SAM**: Simulates Lambda and API Gateway locally for testing.
- **Docker**: Runs a local PostgreSQL database to mimic Aurora.
- **Unit Tests**: Each backend function has tests to catch bugs early.

## Deployment

- **Backend**: Deployed via AWS SAM, setting up Lambda, API Gateway, and other services.
- **Frontend**: Built as a static site, hosted on AWS S3 with CloudFront for fast global access.
- **Database**: Aurora PostgreSQL Serverless is configured in AWS, scaling automatically.