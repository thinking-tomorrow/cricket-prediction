# Generated by Django 3.0.8 on 2020-09-10 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipl', '0008_delete_qualifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='qualifier_type',
            field=models.TextField(default=None),
        ),
    ]