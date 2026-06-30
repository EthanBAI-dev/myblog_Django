#!/bin/bash
cd /home/EthanBAI/myblog_Django
git pull origin personal-website-redesign
source venv/bin/activate
pip install -r requirements.txt -q
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py compilemessages
