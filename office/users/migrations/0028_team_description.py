# Generated by Django 4.2.13 on 2024-07-24 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0027_alter_education_obtain_marks_and_more")]

    operations = [
        migrations.AddField(
            model_name="team",
            name="description",
            field=models.CharField(max_length=500, null=True),
        )
    ]
