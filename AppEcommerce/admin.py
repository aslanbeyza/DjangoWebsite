from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    pass

admin.site.register(BasketProduct)
admin.site.register(Profil)
admin.site.register(Adres)
admin.site.register(Comment)


@admin.register(Brand)
class BrandAdmin(TranslationAdmin):
    pass

@admin.register(Gender)
class GenderAdmin(TranslationAdmin):
    pass

@admin.register(Material)
class MaterialAdmin(TranslationAdmin):
    pass

@admin.register(Gemstone)
class GemstoneAdmin(TranslationAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    pass

@admin.register(Style)
class StyleAdmin(TranslationAdmin):
    pass