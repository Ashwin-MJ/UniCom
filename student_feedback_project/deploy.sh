#!/bin/bash
eval "pip3 install -r requirements.txt"
rm db.sqlite3
eval "python3 manage.py migrate --run-syncdb"
eval "python3 populate.py"
touch ./student_feedback_app/__init__.py
LINE="STATIC_ROOT = os.path.join(BASE_DIR, 'static')"
FILE=./student_feedback_project/settings.py
grep -qF -- "$LINE" "$FILE" || echo "$LINE" >> "$FILE"
yes yes | eval "python3 manage.py collectstatic"
sed -i "/$LINE/d" "$FILE"
eval "python3 manage.py migrate --run-syncdb"
eval "python3 manage.py runserver"
