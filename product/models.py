from django.db import models


#class CareInstructionsModel(models.Model):
#    care_instructions_choices = [
#        ('hand_wash', 'Только ручная стирка'),
#        ('can_be_dried_in_a_washing_machine', 'Можно сушить в сушильной или стиральной машине'),
#        ('can_be_ironed', 'Можно гладить'),
#        ('dry_cleaning', 'Сухая чистка (химчистка)')
#    ]
#    care_instructions = models.CharField(max_length=33, choices=care_instructions_choices, default='hand_wash', verbose_name='Уход')

#    class Meta:
#        abstract = True


#class Category(models.Model):
#    name = models.CharField(max_length=50)

#    def __str__(self):
#        return self.name



class ColorProduct(models.Model):
    name = models.CharField(max_length=40, verbose_name='цвет')

    def __str__(self):
        return self.name


class SizeProduct(models.Model):
    name = models.CharField(max_length=10, verbose_name='размер')

    def __str__(self):
        return self.name


class CollectionProduct(models.Model):
    name = models.CharField(max_length=40, verbose_name='коллекция')

    def __str__(self):
        return self.name


class Boots(models.Model):
    name = models.CharField(max_length=40, verbose_name='кросовки')
    color = models.ManyToManyField(ColorProduct, max_length=40,  verbose_name='цвет кросовок')
    size = models.ManyToManyField(SizeProduct, max_length=40,  verbose_name='размер кросовок')
    image = models.ImageField(verbose_name='Фото', upload_to='content/%Y/%m', blank=True)
    description = models.TextField(verbose_name='О товаре', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    volume = models.CharField(max_length=100, verbose_name='Кол-во', blank=True, null=True)
    collection = models.ManyToManyField(CollectionProduct, max_length=40,  verbose_name='коллекция')

    def __str__(self):
        return self.name

