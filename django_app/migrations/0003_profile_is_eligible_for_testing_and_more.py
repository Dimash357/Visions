# Generated by Django 4.1.7 on 2025-01-12 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0002_remove_profile_is_eligible_for_testing_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_eligible_for_testing',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='passed_testing',
            field=models.BooleanField(default=False),
        ),
    ]