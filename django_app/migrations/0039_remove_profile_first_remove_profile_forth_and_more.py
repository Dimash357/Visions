# Generated by Django 4.1.7 on 2025-01-07 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0038_remove_task_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='first',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='forth',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='second',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='third',
        ),
    ]
