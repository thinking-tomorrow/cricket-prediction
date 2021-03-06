# Generated by Django 3.0.8 on 2020-09-11 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipl', '0009_schedule_qualifier_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='OriginalPointsTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.TextField()),
                ('played', models.IntegerField()),
                ('won', models.IntegerField()),
                ('lost', models.IntegerField()),
                ('points', models.IntegerField()),
                ('nrr', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
