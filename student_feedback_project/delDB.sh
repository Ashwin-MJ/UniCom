#!/bin/bash

rm db.sqlite3
manage.py migrate --run-syncdb
populate.py