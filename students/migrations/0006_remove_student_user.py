# Generated by Django 5.1.7 on 2025-03-29 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_student_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
    ]
