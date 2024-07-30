Flask QR Code Application

This Flask application provides user authentication features and QR code generation with tracking capabilities. It uses Flask, Flask-SQLAlchemy, Flask-Migrate, and Flask-Login to manage user accounts, sessions, and QR code functionalities.
Features

    User Registration: Allows users to create an account with a username, email, and password.
    User Login: Allows users to log into their account.
    Dashboard: Redirects users to a dashboard page upon successful login, where they can generate and view QR codes.
    QR Code Generation: Allows users to generate QR codes for URLs.
    QR Code Tracking: Tracks visits to QR code links and records them.
    Responsive Navbar: Includes links for login, registration, and logout.

Project Structure

    app/ - Contains application code:
        __init__.py - Initializes the Flask application, database, and login manager.
        models.py - Defines the database models, including QR code tracking.
        forms.py - Contains form definitions for registration, login, and QR code generation.
        routes.py - Defines the routes and view functions.
        templates/ - Contains HTML templates:
            base.html - Base template with navbar.
            index.html - Home page template with QR code generation form.
            login.html - Login page template.
            register.html - Registration page template.
            dashboard.html - Dashboard page with QR code management.
        static/ - Contains static files like CSS and JavaScript.

    migrations/ - Contains migration scripts for the database.

    .env - Environment variables for the application.

    config.py - Configuration settings.

    requirements.txt - List of dependencies.

    run.py - Entry point to run the application.

Installation

    Clone the Repository:

    bash

git clone https://github.com/shachaudhary/flask_QR.git
cd flask_QR

Set Up a Virtual Environment:

bash

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install Dependencies:

bash

pip install -r requirements.txt

Set Up the Database:

    Create a .env file with the following content:

    env

FLASK_APP=run.py
FLASK_ENV=development
SQLALCHEMY_DATABASE_URI=sqlite:///site.db
SECRET_KEY=your_secret_key

Initialize the database and create the initial migration:

bash

    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade

Run the Application:

bash

    flask run

    The application will be available at http://127.0.0.1:5000/.

Usage

    Register: Visit /register to create a new account.
    Login: Visit /login to access your account.
    Dashboard: After logging in, you will be redirected to /dashboard, where you can generate and view QR codes.