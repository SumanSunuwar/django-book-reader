# Generated by Django 4.2.16 on 2024-10-06 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0006_remove_readinglist_added_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookstatus',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
