from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Brand, Product, ProductImage, ProductLine


class EditLinkInLine:
    def edit(self, instance):
        if not instance.pk:
            return ""
        url = reverse(
            f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",
            args=[instance.pk],
        )
        return mark_safe(f'<a href="{url}">edit</a>')


class ProductLineInLine(EditLinkInLine, admin.TabularInline):
    model = ProductLine
    readonly_fields = ("edit",)


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductLineInLine,
    ]


class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


admin.site.register(ProductLine, ProductLineAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Brand)
