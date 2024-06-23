#!/bin/bash

echo "Starting unit tests"

python manage.py test apps.core.tests.views.home
# ... more tests