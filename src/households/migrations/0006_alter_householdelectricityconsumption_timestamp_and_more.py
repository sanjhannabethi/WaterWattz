# Generated by Django 4.2.5 on 2023-09-21 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('households', '0005_householdwaterconsumption_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='householdelectricityconsumption',
            name='timestamp',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='householdwaterconsumption',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
