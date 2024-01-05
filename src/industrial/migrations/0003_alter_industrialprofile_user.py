# Generated by Django 4.2.5 on 2023-09-19 04:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('industrial', '0002_industrialprofile_is_industrial_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industrialprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='industrial_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
