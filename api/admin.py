"""
admin.py — Django Admin registrations for all Inventory Hub models.
Each model is registered with a custom ModelAdmin for rich list views,
search, filtering, and inline editing where appropriate.
"""
from django.contrib import admin
from .models import (
    Category, Supplier, Product,
    SaleOrder, SaleItem, StockMovement, UserProfile,
)


# ---------------------------------------------------------------------------
# Category
# ---------------------------------------------------------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display    = ['name', 'color', 'created_date', 'updated_date']
    search_fields   = ['name', 'description']
    ordering        = ['-created_date']
    readonly_fields = ['created_date', 'updated_date']


# ---------------------------------------------------------------------------
# Supplier
# ---------------------------------------------------------------------------
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display    = ['name', 'contact_person', 'email', 'phone', 'created_date']
    search_fields   = ['name', 'email', 'contact_person', 'phone']
    ordering        = ['-created_date']
    readonly_fields = ['created_date', 'updated_date']


# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display    = [
        'name', 'sku', 'category', 'supplier',
        'stock_quantity', 'min_stock_alert', 'status', 'selling_price',
    ]
    search_fields   = ['name', 'sku', 'category', 'supplier', 'barcode']
    list_filter     = ['status', 'category']
    ordering        = ['-created_date']
    readonly_fields = ['created_date', 'updated_date']
    fieldsets = (
        ('🏷️  Identification', {
            'fields': ('name', 'sku', 'barcode', 'status'),
        }),
        ('📂  Categorization', {
            'fields': ('category', 'supplier', 'warehouse'),
        }),
        ('💰  Pricing', {
            'fields': ('purchase_price', 'selling_price'),
        }),
        ('📦  Stock', {
            'fields': ('stock_quantity', 'min_stock_alert', 'expiry_date'),
        }),
        ('🖼️  Media', {
            'fields': ('image', 'image_url'),
            'classes': ('collapse',),
        }),
        ('🕒  Timestamps', {
            'fields': ('created_date', 'updated_date'),
            'classes': ('collapse',),
        }),
    )


# ---------------------------------------------------------------------------
# SaleOrder  (with inline SaleItems)
# ---------------------------------------------------------------------------
class SaleItemInline(admin.TabularInline):
    model           = SaleItem
    extra           = 0
    fields          = ['product_name', 'sku', 'quantity', 'unit_price', 'total']
    readonly_fields = ['total']


@admin.register(SaleOrder)
class SaleOrderAdmin(admin.ModelAdmin):
    list_display    = [
        'order_number', 'customer_name', 'customer_email',
        'total_amount', 'payment_status', 'status', 'created_date',
    ]
    search_fields   = ['order_number', 'customer_name', 'customer_email']
    list_filter     = ['payment_status', 'status']
    ordering        = ['-created_date']
    readonly_fields = ['created_date']
    inlines         = [SaleItemInline]


# ---------------------------------------------------------------------------
# StockMovement
# ---------------------------------------------------------------------------
@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display    = [
        'product_name', 'product_sku', 'type',
        'quantity', 'stock_before', 'stock_after',
        'reason', 'reference', 'created_date',
    ]
    search_fields   = ['product_name', 'product_sku', 'reference', 'reason']
    list_filter     = ['type']
    ordering        = ['-created_date']
    readonly_fields = ['created_date', 'stock_before', 'stock_after']


# ---------------------------------------------------------------------------
# UserProfile
# ---------------------------------------------------------------------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display    = ['user', 'business_name', 'business_email', 'currency', 'tax_rate']
    search_fields   = ['user__username', 'user__email', 'business_name']
    readonly_fields = ['user']
