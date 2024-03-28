from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=35, verbose_name='Название')
    image = models.ImageField(verbose_name='Фото', upload_to='content/%Y/%m', blank=True)
    description = models.TextField(verbose_name='О товаре', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    volume = models.CharField(max_length=100, verbose_name='Кол-во', blank=True, null=True)
    #type_clothing = models.CharField

    def __str__(self):
        return f'{self.name}, {self.volume}'


class CareInstructionsModel(models.Model):
    care_instructions_choices = [
        ('hand_wash', 'Только ручная стирка'),

    ]
    care_instructions = models.CharField(max_length=20, choices=care_instructions_choices, default='hand_wash', verbose_name='Уход')

    class Meta:
        abstract = True


class OuterwearClothingProduct(Product, CareInstructionsModel):
    size = models.CharField(max_length=10, verbose_name='Размер')
    color = models.CharField(max_length=20, verbose_name='Цвет', name='зелённый/бежевый')
    hood = models.CharField(max_length=10, verbose_name='Капюшон')
    silhouette = models.CharField(max_length=40, verbose_name='Силуэт')
    compound = models.CharField(max_length=40, verbose_name='Состав')
    lining_composition = models.CharField(max_length=40, verbose_name='Состав подкладки')
    insulation_composition = models.CharField(max_length=45, verbose_name='Состав утеплителя')
    upper_composition = models.CharField(max_length=45, verbose_name='Состав верха')
    clothing_collection = models.CharField(max_length=35, verbose_name='Коллекция')

    def __str__(self):
        return f'{self.clothing_collection}'


class JeansClothingProduct(Product, CareInstructionsModel):
    size = models.CharField(max_length=10, verbose_name='Размер')
    color = models.CharField(max_length=20, verbose_name='Цвет', name='зелённый/бежевый')
    lining_material = models.CharField(max_length=40, verbose_name='Материал подкладки')
    silhouette = models.CharField(max_length=40, verbose_name='Силуэт')
    fashion = models.CharField(max_length=40, verbose_name='Фасон')
    style = models.CharField(max_length=40, verbose_name='Стиль')
    compound = models.CharField(max_length=40, verbose_name='Состав')
    clothing_collection = models.CharField(max_length=35, verbose_name='Коллекция')

    def __str__(self):
        return f'{self.clothing_collection}'


class Tshirts_and_longsleevesClothingProduct(Product, CareInstructionsModel):
    size = models.CharField(max_length=10, verbose_name='Размер')
    color = models.CharField(max_length=20, verbose_name='Цвет', name='зелённый/бежевый')
    style = models.CharField(max_length=40, verbose_name='Стиль')
    silhouette = models.CharField(max_length=40, verbose_name='Силуэт')
    the_length_of_the_sleeve = models.CharField(max_length=20, verbose_name='Длина рукава')
    drawing = models.CharField(max_length=40, verbose_name='Рисунок')
    compound = models.CharField(max_length=40, verbose_name='Состав')
    clothing_collection = models.CharField(max_length=35, verbose_name='Коллекция')

    def __str__(self):
        return f'{self.clothing_collection}'


class Hoodies_and_sweatshirtsClothingProduct(Product, CareInstructionsModel):
    size = models.CharField(max_length=10, verbose_name='Размер')
    color = models.CharField(max_length=20, verbose_name='Цвет', name='зелённый/бежевый')
    the_length_of_the_sleeve = models.CharField(max_length=20, verbose_name='Длина рукава')
    hood = models.CharField(max_length=10, verbose_name='Капюшон')
    style = models.CharField(max_length=40, verbose_name='Стиль')
    silhouette = models.CharField(max_length=40, verbose_name='Силуэт')
    compound = models.CharField(max_length=40, verbose_name='Состав')
    drawing = models.CharField(max_length=40, verbose_name='Рисунок')
    clothing_collection = models.CharField(max_length=35, verbose_name='Коллекция')

    def __str__(self):
        return f'{self.clothing_collection}'


class TrousersClothingProduct(Product, CareInstructionsModel):
    size = models.CharField(max_length=10, verbose_name='Размер')
    color = models.CharField(max_length=20, verbose_name='Цвет', name='зелённый/бежевый')
    length_trousers = models.CharField(max_length=20, verbose_name='Длина брюк')
    lining_material = models.CharField(max_length=40, verbose_name='Материал подкладки')
    waist_height = models.CharField(max_length=35, verbose_name='Высота талии')
    fashion = models.CharField(max_length=40, verbose_name='Фасон')
    silhouette = models.CharField(max_length=40, verbose_name='Силуэт')
    compound = models.CharField(max_length=40, verbose_name='Состав')
    style = models.CharField(max_length=40, verbose_name='Стиль')
    drawing = models.CharField(max_length=40, verbose_name='Рисунок')
    clothing_collection = models.CharField(max_length=35, verbose_name='Коллекция')

    def __str__(self):
        return f'{self.clothing_collection}'


class ShirtsClothingProduct(Product, CareInstructionsModel):
    size = models.CharField(max_length=10, verbose_name='Размер')
    color = models.CharField(max_length=20, verbose_name='Цвет', name='зелённый/бежевый')
    silhouette = models.CharField(max_length=40, verbose_name='Силуэт')
    compound = models.CharField(max_length=40, verbose_name='Состав')
    the_length_of_the_sleeve = models.CharField(max_length=20, verbose_name='Длина рукава')
    hood = models.CharField(max_length=10, verbose_name='Капюшон')
    style = models.CharField(max_length=40, verbose_name='Стиль')
    drawing = models.CharField(max_length=40, verbose_name='Рисунок')
    clothing_collection = models.CharField(max_length=35, verbose_name='Коллекция')

    def __str__(self):
        return f'{self.clothing_collection}'


class SportClothingProduct(Product, CareInstructionsModel):
    size = models.CharField(max_length=10, verbose_name='Размер')
    color = models.CharField(max_length=20, verbose_name='Цвет', name='зелённый/бежевый')
    fashion = models.CharField(max_length=40, verbose_name='Фасон')
    silhouette = models.CharField(max_length=40, verbose_name='Силуэт')
    compound = models.CharField(max_length=40, verbose_name='Состав')
    style = models.CharField(max_length=40, verbose_name='Стиль')
    fit_type = models.CharField(max_length=35, verbose_name='Тип посадки')
    drawing = models.CharField(max_length=40, verbose_name='Рисунок')
    clothing_collection = models.CharField(max_length=35, verbose_name='Коллекция')

    def __str__(self):
        return f'{self.clothing_collection}'


class ShortsClothingProduct(Product, CareInstructionsModel):
    size = models.CharField(max_length=10, verbose_name='Размер')
    color = models.CharField(max_length=20, verbose_name='Цвет', name='зелённый/бежевый')
    style = models.CharField(max_length=40, verbose_name='Стиль')
    fashion = models.CharField(max_length=40, verbose_name='Фасон')
    silhouette = models.CharField(max_length=40, verbose_name='Силуэт')
    compound = models.CharField(max_length=60, verbose_name='Состав')
    fit_type = models.CharField(max_length=35, verbose_name='Тип посадки')
    drawing = models.CharField(max_length=40, verbose_name='Рисунок')
    clothing_collection = models.CharField(max_length=35, verbose_name='Коллекция')

    def __str__(self):
        return f'{self.clothing_collection}'
