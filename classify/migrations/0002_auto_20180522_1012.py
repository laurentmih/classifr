# Generated by Django 2.0.5 on 2018-05-22 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classify', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nerstring',
            name='status',
        ),
        migrations.AddField(
            model_name='nerstring',
            name='correct_status',
            field=models.NullBooleanField(choices=[(0, 'Incorrect'), (1, 'Correct')]),
        ),
    ]
