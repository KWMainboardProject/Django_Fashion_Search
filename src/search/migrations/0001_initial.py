# Generated by Django 4.1.2 on 2022-11-10 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("label", "0001_initial"),
        ("product", "0001_initial"),
        ("image", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="search_request",
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
                    "state",
                    models.CharField(
                        choices=[
                            ("U", "Undefine"),
                            ("A", "Progress"),
                            ("N", "None"),
                            ("D", "Done"),
                        ],
                        default="U",
                        max_length=1,
                        verbose_name="Search Work State",
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
                    "maincategory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="label.maincategory",
                        verbose_name="Main Categtegory ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="search_result",
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
                ("score", models.FloatField(verbose_name="Score")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.product",
                        verbose_name="Product ID",
                    ),
                ),
                (
                    "request",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="search.search_request",
                        verbose_name="Request ID",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="search_result",
            constraint=models.UniqueConstraint(
                fields=("product", "request"), name="unique search result"
            ),
        ),
        migrations.AddConstraint(
            model_name="search_request",
            constraint=models.UniqueConstraint(
                fields=("image", "maincategory"), name="unique search request"
            ),
        ),
    ]
