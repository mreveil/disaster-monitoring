# Disaster Monitoring Dashboard

This is a web-based dashboard that can be deployed in the event of a widespread natural disaster to crowdsource, contextualize and centralize information.

Reports are crowdsourced and curated from public information on social media and news outlets, augmented with geolocation and other details and shown on a map. This can help first responders and interested parties quickly identify locations with the greatest needs and route resources accordingly.

This project was built as a response to the Aug. 14 2021 earthquake that struck the southern peninsula of Haiti. As a survivor of the 2010 earthquake, I created this project to help and perhaps as a way to make myself useful. I hope it will be used to help save lives in other disasters.

## Features

This is a Dango-based platform and therefore comes with the flexiblity and power afforded by Python and the Django web framework.

- Crowdsourcing information: users can add info to be shown on the dashboard after approval.
- Timeline (coming soon): A timeline of all relevant events is compiled and shown automatically.
- CMS: It also comes prepackaged with a Content Management System (CMS) allowing users to publish all types of contents to keep the public informed.
- Etc.

## Developer Guide

To deploy, the following environment variables (or configVars on Heroku) are required:

- DATABASE_URL
- DB_ENGINE
- DB_NAME
- DEBUG
- SECRET_KEY
- SENTRY_DSN
- SERVER

### To run locally

```
git clone https://github.com/mreveil/disaster-monitoring.git
cd disaster-monitoring
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Acknowledgement

The frontend is based on the Open-source **[Django Template](https://www.creative-tim.com/templates/django)** crafted on top of **Argon Dashboard** and Bootstrap.
