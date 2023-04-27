from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import image_product, product, category


class productAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_name', 'price', 'color_pro']
    search_fields = ['name']


class categoryAdmin(admin.ModelAdmin):
    list_display = ['main_category', 'parent', 'Image']
    search_fields = ['main_category', 'Image']


class imageAdmin(admin.ModelAdmin):
    search_fields = ['product_name__name']
    list_display = ['product_name', 'main_image', 'Image']
    list_editable = ['main_image']


admin.site.register(product, productAdmin)
admin.site.register(image_product, imageAdmin)
admin.site.register(category, categoryAdmin)
admin.site.site_header = "صفحة المستخدم"
admin.site.index_title = 'مكتبة البراء'
admin.site.site_url = "http://64.226.77.150:5050"
admin.site.empty_value_display = 'لا يوجد'
# Register your models here.
