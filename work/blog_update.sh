#!/bin/sh

cd `dirname $0`/..

if [ $# -ne 1 ]; then
  echo "ex) python manage.py blog_update <templates>" 1>&2
  exit 1
fi

python manage.py blog_update $1
