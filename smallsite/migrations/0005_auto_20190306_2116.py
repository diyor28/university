# Generated by Django 2.1.5 on 2019-03-06 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smallsite', '0004_auto_20190306_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grades',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
