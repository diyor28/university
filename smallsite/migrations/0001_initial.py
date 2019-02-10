# Generated by Django 2.1.5 on 2019-02-02 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_address', models.EmailField(default='', max_length=254)),
                ('password', models.CharField(default=None, max_length=120)),
                ('nick_name', models.CharField(default=None, max_length=120)),
                ('full_name', models.CharField(default='', max_length=120)),
                ('gender', models.CharField(default='', max_length=120)),
            ],
        ),
    ]