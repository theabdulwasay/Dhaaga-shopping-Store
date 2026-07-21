from django.contrib import admin
from django.utils.html import format_html
from .models import Fabric, Product, Order, OrderItem, ContactMessage, ChatLog


@admin.register(Fabric)
class FabricAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "fabric", "price", "stock", "is_active", "created_at")
    list_filter = ("fabric", "is_active", "created_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("stock", "is_active")
    readonly_fields = ("created_at",)
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "slug", "fabric", "description")
        }),
        ("Pricing & Inventory", {
            "fields": ("price", "stock", "metres", "is_active")
        }),
        ("Visual", {
            "fields": ("swatch_color_start", "swatch_color_end", "image")
        }),
        ("Metadata", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "unit_price", "subtotal")
    
    def subtotal(self, obj):
        return obj.subtotal
    subtotal.short_description = "Subtotal"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "city", "status", "total", "created_at")
    list_filter = ("status", "city", "created_at")
    search_fields = ("full_name", "phone", "address")
    inlines = [OrderItemInline]
    readonly_fields = ("created_at", "total")
    fieldsets = (
        ("Customer Information", {
            "fields": ("full_name", "phone", "email")
        }),
        ("Delivery Address", {
            "fields": ("address", "city")
        }),
        ("Order Status", {
            "fields": ("status",)
        }),
        ("Metadata", {
            "fields": ("created_at", "total"),
            "classes": ("collapse",)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('city')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "message_preview")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "message")
    readonly_fields = ("created_at",)
    
    def message_preview(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_preview.short_description = "Message"


@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ("session_key", "role", "message_preview", "created_at")
    list_filter = ("role", "created_at")
    search_fields = ("session_key", "message")
    readonly_fields = ("created_at",)
    
    def message_preview(self, obj):
        return obj.message[:40] + "..." if len(obj.message) > 40 else obj.message
    message_preview.short_description = "Message"
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')
