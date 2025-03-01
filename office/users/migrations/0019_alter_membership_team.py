# Generated by Django 4.2.13 on 2024-06-14 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("users", "0018_alter_membership_team")]

    operations = [
        migrations.AlterField(
            model_name="membership",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="members",
                to="users.team",
            ),
        )
    ]
