#!/bin/bash

source ./entrypoint.sh 
exec gunicorn --bind 0.0.0.0:8000 project.wsgi