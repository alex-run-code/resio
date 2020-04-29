# RESIO

Facilitating orientation and relocalisation of medical students in Romania.

## Installation

```bash
py manage.py migrate
py manage.py loaddata initial_data
```


## Data Export

```bash
py manage.py dumpdata website.City website.Specialty website.Candidate website.Hospital website.Paperwork website.Service website.Paperwork_Service --format yaml > website/fixtures/initial_data.yaml
```

