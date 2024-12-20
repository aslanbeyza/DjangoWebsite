from .models import*
from modeltranslation.translator import TranslationOptions,register

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('model', 'description')

@register(Brand)
class BrandTranslationOptions(TranslationOptions):
    fields = ('brand',)

@register(Gender)
class GenderTranslationOptions(TranslationOptions):
    fields = ('gender',)

@register(Material)
class MaterialTranslationOptions(TranslationOptions):
    fields = ('material',)

@register(Gemstone)
class GemstoneTranslationOptions(TranslationOptions):
    fields = ('gemstone',)

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category',)

@register(Style)
class StyleTranslationOptions(TranslationOptions):
    fields = ('style',)

