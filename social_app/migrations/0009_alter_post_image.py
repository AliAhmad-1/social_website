# Generated by Django 5.0.1 on 2024-04-12 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0008_post_likes_post_saves_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d/'),
        ),
    ]