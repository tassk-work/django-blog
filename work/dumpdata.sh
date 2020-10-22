#!/bin/sh

cd `dirname $0`/..

python manage.py dumpdata blog --indent 4 > work/dumpdata.json
