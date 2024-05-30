# Generated by Django 5.0.3 on 2024-05-30 02:02

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CollectionProduct",
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
                        db_index=True, max_length=40, verbose_name="Коллекция"
                    ),
                ),
            ],
            options={
                "verbose_name": "Коллекция",
                "verbose_name_plural": "Коллекции",
            },
        ),
        migrations.CreateModel(
            name="ColorProduct",
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
                    models.CharField(db_index=True, max_length=40, verbose_name="Цвет"),
                ),
            ],
            options={
                "verbose_name": "Цвет",
                "verbose_name_plural": "Цвета",
            },
        ),
        migrations.CreateModel(
            name="Confirm",
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
            ],
        ),
        migrations.CreateModel(
            name="CountryOfManufacture",
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
                        db_index=True,
                        max_length=50,
                        verbose_name="Страна производитель",
                    ),
                ),
            ],
            options={
                "verbose_name": "Страна производитель",
                "verbose_name_plural": "Страны производители",
            },
        ),
        migrations.CreateModel(
            name="Gender",
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
                    models.CharField(db_index=True, max_length=25, verbose_name="Пол"),
                ),
            ],
            options={
                "verbose_name": "Пол",
                "verbose_name_plural": "Пол",
            },
        ),
        migrations.CreateModel(
            name="InsoleMaterialProduct",
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
                        db_index=True, max_length=65, verbose_name="Материал стельки"
                    ),
                ),
            ],
            options={
                "verbose_name": "Материал стельки",
                "verbose_name_plural": "Материалы стелек",
            },
        ),
        migrations.CreateModel(
            name="LiningMaterialProduct",
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
                        db_index=True, max_length=65, verbose_name="Материал подкладки"
                    ),
                ),
            ],
            options={
                "verbose_name": "Материал подкладки",
                "verbose_name_plural": "Материалы подкладок",
            },
        ),
        migrations.CreateModel(
            name="OutsoleMaterialProduct",
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
                        db_index=True, max_length=65, verbose_name="Материал подошвы"
                    ),
                ),
            ],
            options={
                "verbose_name": "Материал подошвы",
                "verbose_name_plural": "Материалы подошв",
            },
        ),
        migrations.CreateModel(
            name="RatingStar",
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
                    "value",
                    models.PositiveSmallIntegerField(
                        default=0, verbose_name="Значение"
                    ),
                ),
            ],
            options={
                "verbose_name": "Звезда рейтинга",
                "verbose_name_plural": "Звёзды рейтинга",
            },
        ),
        migrations.CreateModel(
            name="Shoes",
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
                        db_index=True, max_length=40, verbose_name="Название"
                    ),
                ),
                ("url", models.SlugField(max_length=130)),
                (
                    "brand",
                    models.CharField(blank=True, max_length=100, verbose_name="Бренд"),
                ),
                (
                    "main_image",
                    models.ImageField(
                        blank=True,
                        upload_to="product/%Y/%m",
                        verbose_name="Основное фото",
                    ),
                ),
                (
                    "image_1",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="content/%Y/%m",
                        verbose_name="Фото №1",
                    ),
                ),
                (
                    "image_2",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="content/%Y/%m",
                        verbose_name="Фото №2",
                    ),
                ),
                (
                    "image_3",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="content/%Y/%m",
                        verbose_name="Фото №3",
                    ),
                ),
                ("description", models.TextField(blank=True, verbose_name="О товаре")),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=0,
                        default=0,
                        max_digits=10,
                        verbose_name="Цена, руб.",
                    ),
                ),
                (
                    "discount",
                    models.DecimalField(
                        decimal_places=0,
                        default=0,
                        max_digits=4,
                        null=True,
                        verbose_name="Скидка, %",
                    ),
                ),
                (
                    "stock",
                    models.PositiveIntegerField(blank=True, verbose_name="Осталось"),
                ),
                (
                    "manufacturers_code",
                    models.CharField(
                        blank=True,
                        help_text='"Код товара должен состоять из 5-6 цифр"',
                        max_length=10,
                        verbose_name="Код производителя",
                    ),
                ),
                ("available", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Обувь",
                "verbose_name_plural": "Обуви",
            },
        ),
        migrations.CreateModel(
            name="SizeProduct",
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
                        db_index=True, max_length=10, verbose_name="Размер"
                    ),
                ),
            ],
            options={
                "verbose_name": "Размер",
                "verbose_name_plural": "Размеры",
            },
        ),
        migrations.CreateModel(
            name="UpperMaterialProduct",
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
                        db_index=True, max_length=65, verbose_name="Материал верха"
                    ),
                ),
            ],
            options={
                "verbose_name": "Материал верха",
                "verbose_name_plural": "Материалы верха",
            },
        ),
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=160)),
                ("url", models.SlugField(max_length=160, unique=True)),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="product.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
            },
        ),
        migrations.CreateModel(
            name="Rating",
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
                    "star",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.ratingstar",
                        verbose_name="звезда",
                    ),
                ),
            ],
            options={
                "verbose_name": "Рейтинг",
                "verbose_name_plural": "Рейтинги",
            },
        ),
        migrations.CreateModel(
            name="Review",
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
                    "text",
                    models.TextField(
                        blank=True, max_length=5000, verbose_name="Сообщение"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="product.review",
                        verbose_name="Родитель",
                    ),
                ),
                (
                    "rating",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="product.rating"
                    ),
                ),
            ],
            options={
                "verbose_name": "Отзыв",
                "verbose_name_plural": "Отзывы",
            },
        ),
    ]
