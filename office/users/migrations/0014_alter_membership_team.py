# Generated by Django 4.2.13 on 2024-06-14 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("users", "0013_profile_phone")]

    operations = [
        migrations.AlterField(
            model_name="membership",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="memeber",
                to="users.team",
            ),
        )
    ]
