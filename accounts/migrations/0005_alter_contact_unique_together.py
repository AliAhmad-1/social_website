# Generated by Django 5.0.1 on 2024-04-23 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_contact_user_from_alter_contact_user_to_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contact',
            unique_together={('user_to', 'user_from')},
        ),
    ]