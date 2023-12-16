## Comprehensive API Documentation

  - [Link](https://documenter.getpostman.com/view/20444054/2s9Ykn7gwX)


## Language

- Python v3.10.12

## Framework

- Django v4.2
- Djangorestframework v3.14.0


## Installation
## Step 1 - Download and Install Python
- Download python v3.10.12
- Run the executable file as an administrator
- Add python path to environment variables
## Step 2 - Repository
- Clone the following [repository](https://github.com/mohammadjayeed/e-commerce.git),
```bash
  git clone  https://github.com/mohammadjayeed/e-commerce.git
```
## Step 3 - Virtual Environment
- Make a virtual environment with the following command
```bash
  python -m venv venv
```
-  Activate the virtual environment with the command
```bash
  venv/scripts/activate
```
## Step 4 - Dependencies
- Install dependencies
```bash
  pip install -r requirement.txt
```
## Step 5 - Migrations
- Run the following command to apply it to the database
```bash
  python manage.py migrate
```
## Step 6 - Superuser
- Run the following command to create a superuser to access admin panel by adding the required information. We will require username and password to login to the admin panel
```bash
  python manage.py createsuperuser
```
## Step 7 - Start App
- Start the application by typing the following command
```bash
  python manage.py runserver
```
## Step 8 - Testing the App
- Test the application for models and views by typing the following command
```bash
  python manage.py test
```
# Done !!