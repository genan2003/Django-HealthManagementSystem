# Django Health Management System

This is a web application for managing medical appointments, built with the Django framework. It allows patients to register, find doctors, and book appointments. Doctors can manage their appointments and patient information.

## Features

*   **User Roles:** Separate registration and login for Patients and Doctors.
*   **Patient Features:**
    *   Search for doctors by specialization and location.
    *   Book appointments with available doctors.
    *   View and manage their upcoming and past appointments.
*   **Doctor Features:**
    *   View and manage their appointment schedule.
    *   Approve or decline appointment requests.
    *   View patient information for upcoming appointments.
    *   Create medical recommendations for patients.

## Technologies Used

*   **Backend:** Python, Django
*   **Frontend:** HTML, CSS
*   **Database:** SQLite3

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

*   Python 3.8+
*   pip (Python package installer)

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd Django-HealthManagementSystem
    ```

2.  **Create and activate a virtual environment:**
    *   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install dependencies:**
    A `requirements.txt` file is not included in the project. You will need to install Django and other dependencies manually. Based on the project structure, you will likely need:
    ```bash
    pip install Django
    ```
    You may need to install other packages as well, depending on the project's specific needs.

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be running at `http://127.0.0.1:8000/`.

## How to Use

1.  Start the server and navigate to `http://127.0.0.1:8000/` in your web browser.
2.  Register a new account as either a "Patient" or a "Doctor".
3.  Log in to access your dashboard and the application's features.
