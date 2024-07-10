# Generated by Django 4.2.13 on 2024-07-09 08:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("users", "0024_alter_profile_user")]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="leader",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="teams",
                to=settings.AUTH_USER_MODEL,
            ),
        )
    ]
