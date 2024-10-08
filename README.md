# Read List Manager

A Django-based project for managing reading lists, set up in a production-level environment, with easy-to-follow instructions for local development.

## Prerequisites

Ensure you have the following installed:

- Python (version >= 3.7, recommended 3.12.0)
- Git
- Poetry (for dependency management)

## Setup Instructions

Follow these steps to set up the project locally for development:
Please note that installing poetry and running without python venv is completely fine. which insall poetry on global environment, then peotry install for dependencies (pyrpoject.toml) and straight away running the server following migrations.
1. **Clone the repository**:
    ```bash
    git clone https://github.com/SumanSunuwar/read-list-manager.git
    cd read-list-manager
    ```

2. **Set up a virtual environment**:
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```

4. **Upgrade pip, setuptools, and install Poetry**:
    ```bash
    python -m pip install --upgrade pip setuptools wheel
    pip install poetry
    ```

5. **Install project dependencies**:
    - Install with Poetry:
      ```bash
      poetry install
      ```

6. **Set up local settings**:
    - Create a `local` directory:
      ```bash
      mkdir local
      ```
    - Copy development settings template:
      ```bash
      cp ./config/settings/templates/settings.dev.py ./local/settings.dev.py
      ```
    - For production settings, you can create an empty settings file:
      ```bash
      touch ./local/settings.prod.py
      ```

## Running the Development Server

To run the Django development server:

1. **Activate the virtual environment** (install packages):
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - install packages
      ```bash
      poetry install
    ```

2. **Run the development server**:
    ```bash
    python manage.py runserver
    ```
    or
    ```bash
    poetry run python manage.py runserver
    ```
    from the src folder or
    ```
    poetry run python .src/manage.py runserver
    ```

3. **Database Migration**:
   - makemigrations
    ```bash
    poetry run python manage.py makemigrations
    ```
    - migrate
    ```bash
    poetry run python manage.py migrate
    ```
    - createsuperuser and access admin site ad localhost/admin
    ```bash
    poetry run python manage.py createsuperuser
    ```
    - runserver (dev)
    ```bash
    poetry run python manage.py runserver
    ```
This will start the server locally, and you can visit `http://127.0.0.1:8000` to access the application.

---

### Additional Information

- **Local settings**: All local settings (for development) should go into `./local/settings.dev.py`. This is where any non-production-specific configuration can be overridden by the developer.
- **Production settings**: For production settings, use `./local/settings.prod.py` as required.

### Environment Variables:
The project relies on environment variables prefixed with CORESETTINGS_. Below is an example .env file for configuring your environment:

# Django settings
CORESETTINGS_SECRET_KEY=your_secret_key
CORESETTINGS_DEBUG=true
CORESETTINGS_ALLOWED_HOSTS=localhost,127.0.0.1

# Override local settings if needed
CORESETTINGS_Local_SETTINGS_PATH=./local/settings.prod.py


### Database Setup:
Currently, the project uses SQLite, which is suitable for local development. However, moving to any SQL-based database such as PostgreSQL or MySQL is straightforward with Django. All SQL-based databases are supported efficiently with just a few settings changes.

- **To migrate to a different database:**

- **Install the necessary database driver (e.g., psycopg2 for PostgreSQL).**
- **Update your DATABASES setting in settings.py or local/settings.dev.py for the target database.**
- **Apply migrations (explained below).**


## Database Migrations
   Create migration
   ```bash
   python manage.py makemigrations
   ```
   Migrate db 
   ```bash
   python manage.py migrate
   ```

 ### Collecting Static Files
   In development, static files are served automatically when DEBUG=True. However, for production:

   - **Run collectstatic to gather all static files:**
   ```bash
   python manage.py collectstatic
   ```

   - **In production, with DEBUG=False, static files should be served using a web server like Nginx or Gunicorn. You can also use a CDN for better performance.**


### Scaling for Production
While this guide focuses on local development, Django’s architecture supports smooth scalability for production environments:

- **Switching to a more robust database: Moving from SQLite to a full SQL database like PostgreSQL is simple and improves performance and scalability.**
- **Static file handling: When running in production, static files should be served by a dedicated web server or via a CDN.**
- **Web server setup: Using Gunicorn as an application server, combined with Nginx as a reverse proxy, is a common and efficient setup for serving Django applications in production.**


### Summary
- **This project follows best practices for both development and production setups. It is initially configured with SQLite for simplicity but is easily scalable for larger databases like PostgreSQL or MySQL. The guide provides detailed instructions for getting started with development, applying migrations, and handling static files. For production deployment, additional configurations like serving static files and using web servers like Gunicorn and Nginx can be explored.**
