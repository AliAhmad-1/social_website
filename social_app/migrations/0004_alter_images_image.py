# Generated by Django 5.0.1 on 2024-04-01 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0003_alter_images_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(null=True, upload_to='images/%Y/%m/%d/'),
        ),
    ]
