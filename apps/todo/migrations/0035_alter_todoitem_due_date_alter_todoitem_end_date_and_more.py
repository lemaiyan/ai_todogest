# Generated by Django 4.2.6 on 2023-12-01 06:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0034_alter_todoitem_due_date_alter_todoitem_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='due_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 12, 3, 9, 34, 15, 548023), null=True),
        ),
        migrations.AlterField(
            model_name='todoitem',
            name='end_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 12, 2, 10, 34, 15, 548062), null=True),
        ),
        migrations.AlterField(
            model_name='todoitem',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 12, 2, 9, 34, 15, 548049), null=True),
        ),
    ]
