#!/bin/sh

cd `dirname $0`/..

python manage.py makemessages -l ja --no-location
python manage.py makemessages -l en --no-location
