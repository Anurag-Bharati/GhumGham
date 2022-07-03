# Generated by Django 4.0.1 on 2022-07-03 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itinerary',
            name='places',
            field=models.ManyToManyField(blank=True, to='dashboard.Place'),
        ),
        migrations.AlterField(
            model_name='place',
            name='adventures',
            field=models.ManyToManyField(blank=True, to='dashboard.Adventure'),
        ),
    ]