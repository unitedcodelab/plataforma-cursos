#!/bin/bash

echo "Starting unit tests"

python src/manage.py test apps.core.tests.views.home
# ... more tests