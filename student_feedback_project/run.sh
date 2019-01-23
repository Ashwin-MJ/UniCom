rm db.sqlite3
eval "python3 manage.py migrate --run-syncdb"
eval "python3 populate.py"
eval "python3 manage.py runserver"
