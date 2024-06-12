# Generated by Django 4.2.13 on 2024-06-12 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0008_alter_education_profile")]

    operations = [
        migrations.CreateModel(
            name="ProfileImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=30)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="images/"),
                ),
            ],
        ),
        migrations.RemoveField(model_name="profile", name="image"),
    ]
