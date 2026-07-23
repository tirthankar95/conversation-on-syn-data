# Django Backend Project

This is a Django backend project that implements a RESTful API. Below are the details for setting up and running the project.

## Project Structure

```
django-backend
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps
│   └── api
│       ├── migrations
│       │   └── __init__.py
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── serializers.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── manage.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd django-backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Project

1. Apply migrations:
   ```
   python manage.py migrate
   ```

2. Run the development server:
   ```
   python manage.py runserver
   ```

3. Access the API at `http://127.0.0.1:8000/`.

## API Endpoints

- **Schemas**
  - `GET /api/schemas/` - List all schemas
  - `POST /api/schemas/` - Create a new schema

- **Chats**
  - `GET /api/chats/` - List all chats
  - `POST /api/chats/` - Create a new chat

## Testing

Run the tests using:
```
python manage.py test
```

## License

This project is licensed under the MIT License.