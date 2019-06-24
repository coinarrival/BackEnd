#!/bin/bash

python ./BackEnd/manage.py migrate
python ./BackEnd/manage.py makemigrations
python ./BackEnd/manage.py runserver 0.0.0.0:8000