# Generated by Django 4.1.7 on 2023-06-08 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_profile_phone_number_alter_profile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True, verbose_name='Номер телефона'),
        ),
    ]
