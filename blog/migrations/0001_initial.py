# Generated by Django 3.1 on 2020-10-22 00:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_text', models.CharField(max_length=100)),
                ('aside_text', models.TextField(max_length=1000)),
                ('template_text', models.CharField(blank=True, max_length=20, null=True)),
                ('flags', models.IntegerField(default=0, help_text='AUTHOR_FLAGS_HELP')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_text', models.CharField(blank=True, help_text='BLOG_TITLE_HELP', max_length=100)),
                ('summary_text', models.CharField(blank=True, help_text='BLOG_TITLE_HELP', max_length=1000, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Draft'), (2, 'Private'), (3, 'Public'), (-1, 'Deleted')], default=1)),
                ('search_text', models.CharField(blank=True, help_text='BLOG_TITLE_HELP', max_length=5000)),
                ('template_text', models.CharField(max_length=20)),
                ('flags', models.IntegerField(default=0, help_text='BLOG_FLAGS_HELP')),
                ('view_count', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='BLOG_TITLE_HELP')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.author')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_text', models.CharField(blank=True, max_length=100)),
                ('comment_text', models.TextField(max_length=1000)),
                ('status', models.IntegerField(choices=[(1, 'Unapproved'), (2, 'Approved'), (-1, 'Deleted')], default=1)),
                ('client_text', models.CharField(max_length=20)),
                ('created_date', models.DateTimeField()),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blog')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.comment')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_text', models.CharField(max_length=20)),
                ('order_number', models.IntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.author')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlogCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blog')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.category')),
            ],
        ),
    ]
