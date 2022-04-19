TASKSAPP
Personal project, developed to list tasks and records of it inside a personal account. The project has been built with django. 

This is my first django project,  it could contain some mistakes or bugs, however you can test it.

INSTALLATION
create a virtual environment with "python -m venv venv" in your computer and clon the repository in the same folder.
lift your virtual environment and Install all dependencies using 
"pip install requirements.txt"

MAKE MIGRATIONS
It is needed to migrate all models to sqlite3 so run the commands:
python manage.py makemigrations
python manage.py migrate

RUN SERVER
After doing all of above steps you can lift the server anytime you want to with the command "python manage.py runserver"

go to your browser and load the page, normally the url is localhost:8000, you can check it on your console after lifting up the server