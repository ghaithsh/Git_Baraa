
from django.db import models
from django.forms import ImageField


class category(models.Model):
    main_category = models.CharField(
        max_length=255, blank=False, null=False, unique=True, verbose_name="اسم الصنف")
    parant = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, verbose_name="الصنف الأساسي إن وجد")
    Image = models.ImageField(
        upload_to='media/category/', default="media/category/notfound.png", verbose_name="الصورة")

    def __str__(self):
        return self.main_category


class product(models.Model):
    name = models.CharField(max_length=255, blank=False,
                            null=False, unique=True, verbose_name="الاسم")
    description = models.TextField(
        default="لا يوجد", blank=True, null=True, verbose_name="الوصف")
    color_pro = models.CharField(
        max_length=255, blank=False, null=False, verbose_name="اللون")
    price = models.IntegerField(blank=False, null=False, verbose_name="السعر")
    category_name = models.ForeignKey(
        category, on_delete=models.CASCADE, verbose_name="الصنف")
    active = models.BooleanField(default=True, verbose_name="معروض")

    def __str__(self):
        return self.name


class image_product(models.Model):
    product_name = models.ForeignKey(
        product, on_delete=models.CASCADE, verbose_name="اسم المنتج")
    Image = models.ImageField(upload_to='media/prodcut/',
                              default="media/product/notfound.png", verbose_name="الصورة")
    main_image = models.BooleanField(
        default=False, verbose_name="أساسية")

    def __str__(self):
        return str(self.product_name)
