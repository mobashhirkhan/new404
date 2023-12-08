# CMPUT404-project-socialdistribution

CMPUT 404 Project: Social Distribution

- [Deployed website](https://node-net-46d70235bc29.herokuapp.com/nodenet/login/?next=/nodenet/)
- [Project requirements](https://github.com/uofa-cmput404/project-socialdistribution/blob/master/project.org)

## Contributors / Licensing

Authors:

- Albert Dinh
- Dhruvraj Singh
- Mobashhir Khan
- Daniel Asimiakwini
- Jaspreet Singh Dhami

Generally everything is LICENSE'D under the MIT License by Scripted.

## Running instructions

- Set up a virtual environment through these steps:
  - `virtualenv venv --python=python3.8`
  - `source venv/bin/activate`
  - `pip install -r requirements.txt`
- Run the server with `python manage.py runserver`
- Make migrations with the following commands:
  - `python manage.py makemigrations`
  - `python manage.py migrate`

## Useful resources

- [Django Testing](https://docs.djangoproject.com/en/4.2/topics/testing/)
- [Checkout to a git checkout _commit id_ .](https://medium.com/swlh/using-git-how-to-go-back-to-a-previous-commit-8579ccc8180f#:~:text=Go%20back%20to%20the,make%20will%20be%20lost.)
- Get all remote GitHub branches: `git fetch --all`
- Delete a local branch using git: `git branch -d <branch_name>`

## Technologies used

- Bootstrap and CSS for the frontend
- Django for the backend
