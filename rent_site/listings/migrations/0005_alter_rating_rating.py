# Generated by Django 5.1 on 2024-08-23 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0004_alter_rating_options_alter_rating_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
