#!/bin/bash
set -e  # exit on any error

echo "=== 1. Reset local changes & pull ==="
cd /home/EthanBAI/myblog_Django
git checkout -- locale/*/LC_MESSAGES/django.mo 2>/dev/null || true
git clean -fd locale/ 2>/dev/null || true
git pull origin personal-website-redesign

echo "=== 2. Activate venv ==="
source venv/bin/activate

echo "=== 3. Install deps ==="
pip install -r requirements.txt -q

echo "=== 4. Migrate DB ==="
python manage.py migrate --noinput

echo "=== 5. Compile translations ==="
python manage.py compilemessages

echo "=== 6. Collect static files ==="
python manage.py collectstatic --noinput

echo "=== DONE ==="
