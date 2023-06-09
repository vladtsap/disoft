# Generated by Django 4.2.1 on 2023-05-11 14:49

from django.db import migrations


def combine_names(apps, schema_editor):
    Status = apps.get_model('tasks', 'Status')

    Status.objects.create(name='New')
    Status.objects.create(name='In progress')
    Status.objects.create(name='Done')


class Migration(migrations.Migration):
    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(combine_names),
    ]
