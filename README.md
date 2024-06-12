## Requirements

- Docker
- Docker Compose

## Getting Started

1. Clone this repository to your local machine.
2. Navigate to the project directory in your terminal.
3. Run `docker-compose up --build` to start the Docker containers.
4. Open your web browser and go to `http://localhost:8000/admin` to see the "Hello, World!" message.

## Accessing admin

You need to create a super admin:
- on the terminal run the command `docker-compose run app python manage.py shell`
- followed by `from django.contrib.auth.models import User`
- Create the super user `User.objects.create_superuser('admin', 'admin@localhost.com',  'admin')` and presse enter
- On your browser navigate to `http://localhost:8000/admin` and login with the username `admin` and password `admin`
- You can create a to do and see what happens after saving it watch the logs
