# Generated by Django 5.1 on 2024-09-01 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0021_alter_booking_options_alter_review_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='description',
            field=models.TextField(default='No description'),
        ),
        migrations.AddField(
            model_name='city',
            name='image_filename',
            field=models.ImageField(blank=True, null=True, upload_to='city_images/'),
        ),
    ]
