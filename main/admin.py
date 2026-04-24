from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'slug')
    search_fields = ('name',)
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class MediaInline(admin.TabularInline):
    model = Media
    extra = 1


class PropertyInline(admin.TabularInline):
    model = Property
    extra = 1


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'amount', 'category', 'seller')
    list_filter = ('category', 'seller', 'country')
    search_fields = ('name', 'brand')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [MediaInline, PropertyInline, ChoiceInline]


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'main')


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product')


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product')
    inlines = [VariantInline]


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'choice', 'delta_price')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'percentage', 'new_price', 'end_date')
    list_filter = ('end_date',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rate', 'created_at')
    list_filter = ('rate', 'created_at')
    search_fields = ('text',)


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'active', 'end_date')
    list_filter = ('active',)
    search_fields = ('title',)