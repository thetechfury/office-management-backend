# Generated by Django 4.2.13 on 2024-07-02 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("leave_management", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="leaveapplication",
            name="attachment",
            field=models.FileField(blank=True, null=True, upload_to="application_file"),
        )
    ]
