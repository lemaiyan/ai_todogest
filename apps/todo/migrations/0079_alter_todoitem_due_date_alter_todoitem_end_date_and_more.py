# Generated by Django 5.0.6 on 2024-07-08 21:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0078_alter_todoitem_due_date_alter_todoitem_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='due_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 7, 11, 0, 19, 2, 636413), null=True),
        ),
        migrations.AlterField(
            model_name='todoitem',
            name='end_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 7, 10, 1, 19, 2, 636505), null=True),
        ),
        migrations.AlterField(
            model_name='todoitem',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 7, 10, 0, 19, 2, 636471), null=True),
        ),
    ]