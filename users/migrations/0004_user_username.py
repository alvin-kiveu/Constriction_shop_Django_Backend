# Generated by Django 5.0.2 on 2024-03-12 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='default_username', max_length=150, unique=True),
            preserve_default=False,
        ),
    ]