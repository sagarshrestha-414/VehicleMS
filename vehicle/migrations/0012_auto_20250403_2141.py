# Generated by Django 3.2.9 on 2025-04-03 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0011_auto_20220323_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='mechanic',
            name='mobile',
            field=models.CharField(max_length=10),
        ),
    ]
