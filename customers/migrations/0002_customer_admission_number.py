# Generated by Django 5.1.2 on 2024-11-11 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='admission_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
