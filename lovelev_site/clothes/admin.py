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
    list_filter = ('available', )
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ImageInline, ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class InformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(MenuItem, MenuItemMPTTModelAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Information, InformationAdmin)
