# Generated by Django 4.2.6 on 2023-11-23 00:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0009_alter_todoitem_due_date_alter_todoitem_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='due_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 25, 0, 3, 37, 707527), null=True),
        ),
        migrations.AlterField(
            model_name='todoitem',
            name='end_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 24, 1, 3, 37, 707590), null=True),
        ),
        migrations.AlterField(
            model_name='todoitem',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 24, 0, 3, 37, 707567), null=True),
        ),
    ]
