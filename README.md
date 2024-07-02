

# Backend Django Project Only Authentication

This project is a Django-based web application using Django Rest Framework (DRF) for authentication using jwt with email verification.

## Running the Project with Docker

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd chatinit_backend
   ```

2. Build and start the Docker containers:
   ```bash
   docker-compose up --build -d
   ```

3. Open your browser and navigate to `http://localhost:8000`.

## Running the Project with Virtualenv

### Prerequisites

- [Python ^3.10](https://www.python.org/downloads/)
- [Virtualenv](https://pypi.org/project/virtualenv/)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd chatinit_backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Apply migrations:
   ```bash
   python manage.py migrate
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Open your browser and navigate to `http://localhost:8000`.

## Environment Variables

Ensure you have a `.env` file in the root of your project with the following content:

```dotenv
DATABASE_NAME=myproject
DATABASE_USER=myprojectuser
DATABASE_PASSWORD=myprojectpassword
DATABASE_HOST=db
DATABASE_PORT=5432
SECRET_KEY=your_secret_key
DEBUG=True
```
```

By following these instructions, you will have a fully functional Django project that can be run using Docker for containerized deployment or using a virtual environment for local development.