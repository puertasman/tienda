from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    #list_display = ['name', 'slug']
    #prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'parent', 'is_subcategory')
    list_filter = ('parent',)
    search_fields = ('name',)
    raw_id_fields = ('parent',)

    def is_subcategory(self, obj):
        return obj.parent is not None
    is_subcategory.boolean = True
    is_subcategory.short_description = 'Is Subcategory?'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    #list_display = ['name', 'slug', 'price',
    #                'available', 'created', 'updated']
    #list_filter = ['available', 'created', 'updated']
    #list_editable = ['price', 'available']
    #prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'price', 'category']
    list_filter = ['category']
    search_fields = ['name', 'category__name']
    raw_id_fields = ['category']