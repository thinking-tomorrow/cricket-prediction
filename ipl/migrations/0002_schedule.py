# Generated by Django 3.1 on 2020-08-22 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teams', models.TextField()),
                ('date', models.TextField()),
                ('day', models.TextField()),
                ('time', models.TextField()),
                ('city', models.TextField()),
            ],
        ),
    ]
