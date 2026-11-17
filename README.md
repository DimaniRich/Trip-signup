# Study Abroad Trip Sign-Up

A small Flask app where students register interest in a study abroad trip. Students fill in their name, email and major; signups are saved to a SQLite database and listed on a password-protected admin page.

## Features

- Sign-up form (`/`) with name, email and major
- Thank-you page (`/thanks`) after submitting
- Admin page (`/admin`) listing every signup, protected by a password
- Responsive layout built with Bootstrap 5
- Data stored in `signups.db` using Python's built-in `sqlite3` module

## Requirements

- Python 3.14
- [Pipenv](https://pipenv.pypa.io/)

## Setup

Install the dependencies (Flask, plus pytest for development):

```
pipenv install --dev
```

Create a `.env` file in the project folder with the admin password:

```
ADMIN_PASSWORD=choose-a-strong-password
```

`.env` is listed in `.gitignore`, so the password is never committed. If `ADMIN_PASSWORD` isn't set, the admin page stays locked.

## Running the app

```
pipenv run python app.py
```

Then open http://127.0.0.1:5000.

Start the app with `pipenv run` so the password in `.env` is loaded. Running `python app.py` directly skips the `.env` file.

## Admin page

Go to http://127.0.0.1:5000/admin. The browser shows a login box: enter any username and the password from `.env`.

The admin login uses HTTP Basic authentication, which doesn't encrypt the password by itself. That's fine on your own computer, but serve the app over HTTPS if you deploy it.

## Running the tests

```
pipenv run pytest
```

The tests use Flask's test client and a temporary database, so they never touch your real `signups.db`.

## Project structure

```
app.py               Flask app: routes and database code
templates/
  base.html          Shared Bootstrap layout
  signup.html        Sign-up form
  thanks.html        Thank-you page
  admin.html         Signup list for admins
test_app.py          pytest tests
Pipfile              Dependencies
.gitignore           Keeps .env and signups.db out of git
```
