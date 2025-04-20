How to test the UI
1. start backend server:
sam local start-api \
--template CloudFormation/dev_yaml/template-local.yaml \
--docker-network task_management_network
2. Run the React App:
cd frontend
npm start

Before running npm start, let's install all dependencies via this command:
npm install
This command reads the package.json file and installs all dependencies listed in it, creating a new node_modules directory with all required packages.

