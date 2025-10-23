# Atlas

Atlas is a Django-based student information system designed to manage academic information for the Faculty of Natural and Agricultural Sciences. It provides a platform for students to view their academic progress and for the faculty to manage lecturers' profiles, academic documents, qualifications and modules.

## Features

*   **Student Management:** Allows for student registration, login and profile management.
*   **Academic Records:** Students can view their enrolled qualification, academic progress and module details.
*   **Course Catalog:** Publicly accessible views for browsing available qualifications and modules.
*   **Lecturer Profiles:** Displays profiles for lecturers, including their biography, expertise and contact information.
*   **Academic Resources:** A dedicated section for important academic rules and documents.
*   **Search and Filtering:** Users can easily search and filter through qualifications, modules and lecturers.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/atlas.git
    cd atlas
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply the database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser to access the admin panel:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000`.

## Usage

*   **Admin Panel:** Access the Django admin panel at `/admin` to manage all data, including students, lecturers, qualifications and modules.
*   **Student Portal:** Students can sign up, log in and access their dashboard to view their academic information.
*   **Public Views:** Browse through the list of available programs, modules and lecturers without needing to log in.

## Dependencies

The main dependencies used in this project are:

*   Django
*   django-import-export

You can find the full list of dependencies in the `requirements.txt` file.