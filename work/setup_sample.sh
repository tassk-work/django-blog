#!/bin/sh

cd `dirname $0`/..

python manage.py migrate

python manage.py shell <<EOF
from django.contrib.auth.models import Group, User, Permission
User.objects.create_superuser('admin', 'admin@localhost', 'password')
group = Group(name='blog')
group.save()
group.permissions.set(Permission.objects.filter(id__range=(33,48)))
group.save()
user = User.objects.create_user('sample', 'sample@localhost', 'password')
user.is_staff = True
user.groups.set([group])
user.save()
EOF

python manage.py loaddata work/dumpdata.json
