# Generated by Django 4.2.13 on 2024-06-12 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0006_alter_education_degree_delete_degree")]

    operations = [
        migrations.AddField(
            model_name="education",
            name="total_marks",
            field=models.DecimalField(decimal_places=2, default=223, max_digits=6),
            preserve_default=False,
        )
    ]
