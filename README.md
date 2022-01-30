# Quiz game

This is a mini project to demonstrate the ability to work with Django REST framework

## Requirements

The project was tested on:
+ [Python 3.9](https://www.python.org/downloads/release/python-390/)
+ [Sqlite3](https://www.sqlite.org/download.html)

## Getting Started

In order to install the project follow next few steps:

```sh
  # Clone the repository
  git clone https://github.com/Georg1703/Quiz.git
  
  # Move into project directory
  cd Quiz
  
  # Create virtual environment
  python -m venv venv # or python3 -m venv venv if you are on Mac/Linux
  
  # Activate venv if you are on windows
  venv\Scripts\activate # or source venv/bin/activate if you are on Mac/Linux
  
  # Install all requirements for project
  pip install -r requirements.txt
  
  # Migrate database tables
  python manage.py migrate
  
  # To be sure that everything is ok, run the tests
  python manage.py test quiz.tests
  python manage.py test account.tests
  
  Enjoy !!!
```

## Usage

To be abble to use the project follow next steps:

```sh
# Create superuser (only superuser has right to create, update or delete quizzes, questions and answers)
python manage.py createsuperuser

# Start Django developement server
python manage.py runserver

# ALL ENDPOINTS STARTS WITH localhost:8000/api/

# Visit endpoint accounts/login/ to get access token
# Visit endpoint quizzes/ to create one quiz
# Visit endpoint questions/ to create one question
# Visit endpoint answers/ to create one answer

# After creating all this stuff you can register other users by visiting endpoint accounts/register/
# Then access endpoint /questions/question_id/answers/answer_id/ to post response for one question

# For exhaustive information about all endpoints please visit localhost:8000/swagger/
```
