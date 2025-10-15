# TextInsight Backend Setup

This is the backend of the **TextInsight** project. Below are the steps to set up the project, including how to install dependencies, run the server, and seed the database for testing purposes.

## Project Setup

1. **Clone the Repository**

   Start by cloning the repository to your local machine:

   ```bash
   git clone https://gittoken@github.com/TalhaAhsanSh/textinsight-backend.git
   cd textinsight
   ```

2. **Create and Activate Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies. If you don't already have a virtual environment set up, create and activate one using the following commands:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install Dependencies**

   Install the required dependencies from the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

1. **Run the Development Server**

   Start the Django development server to test the project locally:

   ```bash
   python manage.py runserver
   ```

## Seeding the Database

We have created a seeder file named `seed.seeder.py` to pre-populate the database with test data (students, teachers, classes, assignments, etc.).

1. **Running the Seeder**

   To seed the database with test data, run the following command:

   ```bash
   python seed.seeder.py
   ```

   This will generate:
   - 50 students
   - 3 teachers
   - 4 classes
   - 5 assignments
   - Media objects for profile pictures (random image URLs)

## Contributing

1. **Pull the Latest Changes**

   Before starting to work on the project, make sure to pull the latest changes from the repository:

   ```bash
   git pull origin main
   ```

2. **Commit and Push Your Changes**

   After making your changes, add, commit, and push your changes to the repository:

   ```bash
   git add .
   git commit -m "Your message here"
   git push origin main
   ```

