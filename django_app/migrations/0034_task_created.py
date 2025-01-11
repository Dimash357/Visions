# Generated by Django 4.1.7 on 2025-01-07 11:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0033_task_recipient_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='created',
            field=models.DateTimeField(blank=True, db_column='created_db_column', db_index=True, db_tablespace='created_db_tablespace', default=django.utils.timezone.now, error_messages=False, help_text='<small class="text-muted">DateTimeField</small><hr><br>', null=True, verbose_name='Дата и время создания'),
        ),
    ]
