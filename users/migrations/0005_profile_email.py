# Generated by Django 4.1.7 on 2023-06-05 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_first_name_alter_profile_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='kunasyl@mail.ru', max_length=254, unique=True, verbose_name='Почта'),
            preserve_default=False,
        ),
    ]
