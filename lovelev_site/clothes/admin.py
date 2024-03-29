from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin

from .models import *


class MenuItemMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20


class ImageInline(admin.TabularInline):
    fk_name = 'clothes'
    model = Image


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time_create', 'cat', 'available', 'popular')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'available', )
    list_editable = ('available', )
    list_filter = ('available', 'cat')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ImageInline, ]
    save_on_top = True


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_html_photo')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    fields = ('name', 'slug', 'photo', 'get_html_photo')
    readonly_fields = ('get_html_photo',)

    def get_html_photo(self, object):
        return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Миниатюра"


class InformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class TableSizesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'russianSize', 'chest', 'waist', 'hip')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


admin.site.register(MenuItem, MenuItemMPTTModelAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Information, InformationAdmin)
admin.site.register(TableSizes, TableSizesAdmin)