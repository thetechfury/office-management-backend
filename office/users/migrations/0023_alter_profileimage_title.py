# Generated by Django 4.2.13 on 2024-06-25 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0022_alter_profileimage_profile")]

    operations = [
        migrations.AlterField(
            model_name="profileimage",
            name="title",
            field=models.CharField(blank=True, max_length=30, null=True),
        )
    ]
