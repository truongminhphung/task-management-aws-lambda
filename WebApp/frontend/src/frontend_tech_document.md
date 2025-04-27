src/services/api.js: This file will handle requests to your backend.
withCredentials: true ensures the HTTP-only JWT cookie is sent and received.
The login function sends a POST request to /login and handles success or error responses.

src/components/auth/Login.js: This component will render the login form and handle user input.
src/pages/LoginPage.js: This page will use the Login component and handle navigation.

App.js: Include routing between the login page and homepage.



How to test the UI
1. start backend server:
sam local start-api \
--template CloudFormation/dev_yaml/template-local.yaml \
--docker-network task_management_network
2. Run the React App:
cd frontend
npm start
