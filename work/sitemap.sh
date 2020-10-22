#!/bin/sh

cd `dirname $0`/..

python manage.py ping_google /sitemap.xml
