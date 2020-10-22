#!/bin/sh

cd `dirname $0`/..

python  manage.py makemigrations blog
#python  manage.py sqlmigrate
python manage.py migrate
