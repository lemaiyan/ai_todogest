# Generated by Django 5.0.6 on 2024-07-17 21:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0089_alter_todoitem_due_date_alter_todoitem_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='due_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 7, 20, 0, 4, 49, 223690), null=True),
        ),
        migrations.AlterField(
            model_name='todoitem',
            name='end_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 7, 19, 1, 4, 49, 223713), null=True),
        ),
        migrations.AlterField(
            model_name='todoitem',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 7, 19, 0, 4, 49, 223705), null=True),
        ),
    ]