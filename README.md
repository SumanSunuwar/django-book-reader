# Read List Manager

A Django-based project for managing reading lists, set up in a production-level environment, with easy-to-follow instructions for local development.

## Prerequisites

Ensure you have the following installed:

- Python (version >= 3.7, recommended 3.12.0)
- Git
- Poetry (for dependency management)

## Setup Instructions

Follow these steps to set up the project locally for development:

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

1. **Activate the virtual environment** (if not already activated):
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```

2. **Run the development server**:
    ```bash
    python manage.py runserver
    or
    poetry run python manage.py runserver
    from the src folder or
    poetry run python .src/manage.py runserver
    ```

This will start the server locally, and you can visit `http://127.0.0.1:8000` to access the application.

---

### Additional Information

- **Local settings**: All local settings (for development) should go into `./local/settings.dev.py`. This is where any non-production-specific configuration can be overridden by the developer.
- **Production settings**: For production settings, use `./local/settings.prod.py` as required.

