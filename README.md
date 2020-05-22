# RESIO

[![Build Status](https://travis-ci.org/megalex97/resio.svg?branch=master)](https://travis-ci.org/megalex97/resio)

Facilitating orientation and relocalisation of medical students in Romania.
RESIO is a web platform allowing romanian students to estimate the grade they will need, or the options they will have after the final medecine exam, called the Residana.


## Installation

```bash
pip install -r requirements.txt
virtualenv env
py manage.py migrate
py manage.py loaddata initial_data
py manage.py runserver
```

## Data Export

How to save data in the fixtures

```bash
py manage.py dumpdata website.City website.Specialty website.Candidate website.Hospital website.Paperwork website.Service website.Paperwork_Service --format yaml > website/fixtures/initial_data.yaml
```

## Testing 

To launch tests, type the following command. The tests are automatically launched by travis, but you can launch them yourself using this command : 

```bash
py manage.py test
```

## How to start website

To start the website from your computer, type :
```bash
py manage.py runserver
```

## Launching coverage

```bash
coverage run --source='.' --omit='env*' manage.py test
coverage report
```

## Heroku

To deploy on Heroku, follow those steps:

### Prerequisites 

1. Have git installed
2. Heroku Account – sign up here
3. Download the Heroku Toolbelt – a command line application for managing your Heroku account
3. Run heroku login in your terminal or command prompt and fill in your Heroku credentials

### Configuring django apps for heroku


1. Create a requirements.txt file in the root folder with such content inside

2. Create a Procfile with this line inside : 
```bash
web: gunicorn heroku_blog.wsgi
```

3. Make sure your static files settings are well configured

### Deploying

1. First, navigate to your project

```bash
cd Projects/name-of-website
```

2. make sure everything is commited

```bash
git init
git add .
git commit -m "My site ready for deployment."
```

3. Create a heroku app and push on it

```bash
heroku create name-of-website
git push heroku master
```



