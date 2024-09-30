# Django Book Manager Application

Simple book manager application to search books and add to favorites.

## Features
- User authentication (sign up, login, logout)
- Password reset and change functionality
- Search books and view details
- Add/remove books to favorites
- Access book view history
- Add/ read comments for books
- Responsive UI built with Bootstrap
- PostgreSQL database integration
- Google Books API integration
- Deployed on Render
- Email notifications via Gmail for password reset

## Prerequisites
Before setting up this project, ensure have the following installed:
- Python 3.9 or above
- PostgreSQL
- Git
- Render account (for deployment)
- Gmail account for sending emails

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/KSburna/my_book_manager
cd my_book_manager
```
## 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure PostgreSQL Database

Update `settings.py` with the PostgreSQL credentials.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_name',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': 'db_host',
        'PORT': 'db_port',
    }
}
```

## 5. Run Migrations

```bash
python manage.py migrate
```

## 6. Create a Superuser

```bash
python manage.py createsuperuser
```

## 7. Collect Static Files

```bash
python manage.py collectstatic
```

## 8. Run the Development Server

```bash
python manage.py runserver
```

Access the app at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## 8. Run the Unit tests

```bash
python manage.py test
```