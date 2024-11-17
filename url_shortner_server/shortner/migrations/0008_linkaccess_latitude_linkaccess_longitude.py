# Generated by Django 4.1.3 on 2024-11-17 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortner', '0007_linkaccess_city_linkaccess_country_linkaccess_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkaccess',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='linkaccess',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]