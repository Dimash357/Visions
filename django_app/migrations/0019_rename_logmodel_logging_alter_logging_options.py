# Generated by Django 4.1.7 on 2023-03-11 13:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_app', '0018_rename_task_todo_alter_todo_options'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LogModel',
            new_name='Logging',
        ),
        migrations.AlterModelOptions(
            name='logging',
            options={'ordering': ('-datetime', 'url'), 'verbose_name': 'Log', 'verbose_name_plural': 'Logs'},
        ),
    ]
