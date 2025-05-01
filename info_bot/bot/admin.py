from turtledemo.penrose import start

from django.contrib import admin
from .models import Category, SubCategory, User, OrganisationCategory, Organisation


@admin.register(OrganisationCategory)
class OrganisationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('tg_id','user_name','number',)
    search_fields = ('tg_id','user_name','number',)

@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','category')
    search_fields = ('name', 'description','category')



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'has_file', 'has_image')
    list_filter = ('category',)
    search_fields = ('name', 'text')
    
    def has_file(self, obj):
        return bool(obj.file)
    has_file.short_description = 'Есть файл'
    has_file.boolean = True
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.short_description = 'Есть изображение'
    has_image.boolean = True
