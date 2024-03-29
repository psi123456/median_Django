# Generated by Django 5.0 on 2024-01-12 00:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "modelservice",
            "0002_alter_imagemodel_options_alter_imagemodel_image_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="PredictionResult",
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
                ("x1", models.IntegerField()),
                ("y1", models.IntegerField()),
                ("x2", models.IntegerField()),
                ("y2", models.IntegerField()),
                ("confidence", models.FloatField()),
                ("class_id", models.IntegerField()),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="modelservice.imagemodel",
                    ),
                ),
            ],
            options={
                "db_table": "prediction_results",
            },
        ),
    ]
