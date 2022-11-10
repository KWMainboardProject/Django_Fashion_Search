# Generated by Django 4.1.2 on 2022-11-10 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("label", "0001_initial"),
        ("image", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ImageAttributesTable",
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
                ("img_url", models.ImageField(upload_to="", verbose_name="Image URL")),
                (
                    "attributes_type",
                    models.CharField(max_length=20, verbose_name="Attributes Type"),
                ),
                ("data", models.JSONField(default=dict, verbose_name="Data JSON")),
            ],
            options={"db_table": "ImageAttributesTable", "managed": False,},
        ),
        migrations.CreateModel(
            name="pipe_work_state",
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
                (
                    "subcategory",
                    models.CharField(
                        choices=[
                            ("U", "Undefine"),
                            ("A", "Progress"),
                            ("N", "None"),
                            ("D", "Done"),
                        ],
                        default="U",
                        max_length=1,
                        verbose_name="Sub Category Work State",
                    ),
                ),
                (
                    "pattern",
                    models.CharField(
                        choices=[
                            ("U", "Undefine"),
                            ("A", "Progress"),
                            ("N", "None"),
                            ("D", "Done"),
                        ],
                        default="U",
                        max_length=1,
                        verbose_name="Pattern Work State",
                    ),
                ),
                (
                    "maincolor",
                    models.CharField(
                        choices=[
                            ("U", "Undefine"),
                            ("A", "Progress"),
                            ("N", "None"),
                            ("D", "Done"),
                        ],
                        default="U",
                        max_length=1,
                        verbose_name="Main Color Work State",
                    ),
                ),
                (
                    "subcolor",
                    models.CharField(
                        choices=[
                            ("U", "Undefine"),
                            ("A", "Progress"),
                            ("N", "None"),
                            ("D", "Done"),
                        ],
                        default="U",
                        max_length=1,
                        verbose_name="Sub Color Work State",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="image.request_image",
                        verbose_name="Image",
                    ),
                ),
                (
                    "main",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="label.maincategory",
                        verbose_name="Main Category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="image_attributes",
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
                (
                    "obj_idx",
                    models.PositiveSmallIntegerField(verbose_name="Attributes"),
                ),
                (
                    "attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="label.attributes",
                        verbose_name="Attributes",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="image.request_image",
                        verbose_name="Image",
                    ),
                ),
            ],
        ),
    ]
