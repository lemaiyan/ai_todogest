# Generated by Django 4.2.6 on 2023-12-07 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('google_oauth', '0005_remove_googleuser_ggogle_user_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='googleusertokens',
            name='allow_digest',
            field=models.BooleanField(default=True),
        ),
    ]
