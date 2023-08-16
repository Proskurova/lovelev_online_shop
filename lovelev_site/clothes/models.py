from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from multiselectfield import MultiSelectField


class MenuItem(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    url = models.CharField('Ссылка', max_length=255)
    position = models.PositiveIntegerField('Позиция', default=1)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['position']

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    SIZE_CHOICES = (('XS', 'XS'),
                    ('S', 'S'),
                    ('M', 'M'),
                    ('L', 'L'),
                    ('XL', 'XL'))

    sizes = MultiSelectField(choices=SIZE_CHOICES,
                             max_choices=5,
                             max_length=17, verbose_name="Размеры")
    description = models.TextField(blank=True, verbose_name="Описание")
    available = models.BooleanField(default=True, verbose_name="Наличие")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})


class Image(models.Model):
    clothes = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    default = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})









