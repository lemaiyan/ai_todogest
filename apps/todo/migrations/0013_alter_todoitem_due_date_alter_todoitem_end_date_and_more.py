# Generated by Django 4.2.6 on 2023-11-23 20:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0012_alter_todoitem_due_date_alter_todoitem_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='due_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 25, 20, 8, 15, 306169), null=True),
        ),
        migrations.AlterField(
            model_name='todoitem',
            name='end_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 24, 21, 8, 15, 306199), null=True),
        ),
        migrations.AlterField(
            model_name='todoitem',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 24, 20, 8, 15, 306189), null=True),
        ),
    ]
