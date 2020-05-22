# RESIO

Facilitating orientation and relocalisation of medical students in Romania.
Rajouter + d'infos

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

Comment lancer les tests et le coverage, dire que c lancé automatiquement par travis

## How to start website



## Heroku

Comment déployer le site sur heroku