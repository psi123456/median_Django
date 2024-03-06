# Generated by Django 5.0 on 2024-01-12 12:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("modelservice", "0004_remove_predictionresult_class_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="predictionresult",
            name="image",
        ),
        migrations.AddField(
            model_name="predictionresult",
            name="image_path",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]