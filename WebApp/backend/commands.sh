# This script is used to set up the database for the task management application.
docker run -d -e POSTGRES_DB=tasks-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -p 5432:5432 --name task_management_db postgres:latest --network task_management_network

# connect to the PostgreSQL database
docker exec -it task_management_db psql -U postgres -d tasks-db

