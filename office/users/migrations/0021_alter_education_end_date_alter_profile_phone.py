# Generated by Django 4.2.13 on 2024-06-25 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0020_alter_user_role")]

    operations = [
        migrations.AlterField(
            model_name="education", name="end_date", field=models.DateField()
        ),
        migrations.AlterField(
            model_name="profile", name="phone", field=models.CharField(max_length=13)
        ),
    ]
