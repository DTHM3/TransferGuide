# Generated by Django 4.1.6 on 2023-04-17 05:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transferguideApp', '0005_courserequest_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courserequest',
            name='user',
            field=models.ForeignKey(default='NO USER', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
