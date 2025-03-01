# Generated by Django 4.2.13 on 2024-06-06 05:13

from django.db import migrations, models
import users.custom_managers


class Migration(migrations.Migration):

    dependencies = [("users", "0001_initial")]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[("objects", users.custom_managers.CustomUserManager())],
        ),
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("enduser", "End User"),
                    ("accountant", "Accountant"),
                    ("manager", "Manager"),
                    ("admin", "Admin"),
                ],
                default=("enduser", "End User"),
                max_length=30,
            ),
        ),
    ]
