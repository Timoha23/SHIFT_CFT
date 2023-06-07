#!/bin/sh
echo "start migrate"
alembic upgrade head
echo "end migrate"
echo "start create admin"
python3 utils/create_admin.py
echo "end create admin"
"$@"