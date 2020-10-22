#!/bin/sh

cd `dirname $0`/..

python manage.py migrate --fake blog zero
rm -fr blog/migrations/*
touch blog/migrations/__init__.py

python manage.py makemigrations blog
python manage.py migrate --fake-initial
