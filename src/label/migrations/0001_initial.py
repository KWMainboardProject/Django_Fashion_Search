# Generated by Django 4.1.2 on 2022-11-08 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AttributeIndexTable",
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
                ("data", models.JSONField(default=dict, verbose_name="Data JSON")),
            ],
            options={"db_table": "AttributeIndexTable", "managed": False,},
        ),
        migrations.CreateModel(
            name="AttributeTable",
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
                    "maincategory",
                    models.CharField(max_length=20, verbose_name="Main Category"),
                ),
                (
                    "attributes",
                    models.CharField(max_length=20, verbose_name="Attributes"),
                ),
                ("data", models.JSONField(default=dict, verbose_name="Data JSON")),
            ],
            options={"db_table": "AttributeTable", "managed": False,},
        ),
        migrations.CreateModel(
            name="Maincategory",
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
                    "name",
                    models.CharField(
                        max_length=20, unique=True, verbose_name="Main Category"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AttributesType",
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
                ("name", models.CharField(max_length=20, verbose_name="Type")),
                (
                    "main",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="label.maincategory",
                        verbose_name="Main Category ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Attributes",
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
                ("data", models.JSONField(default=dict, verbose_name="Data JSON")),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="label.attributestype",
                        verbose_name="Type",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="attributestype",
            constraint=models.UniqueConstraint(
                fields=("main", "name"), name="unique type"
            ),
        ),
    ]
