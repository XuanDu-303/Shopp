from django.contrib.auth.models import Group
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from . models import Cart, Category, Customer, OrderPlaced, Product, Wishlist, Review

admin.site.register(Category)

@admin.register(Product)
class ProductModelsAdmin(admin.ModelAdmin):
  list_display = ['id', 'title', 'discounted_price', 'quantity', 'category', 'product_image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
  list_display = ['id', 'user', 'locality', 'city', 'state', 'zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
  list_display = ['id', 'user', 'products', 'quantity']
  def products(self, obj):
    link = reverse("admin:app_product_change", args=[obj.product.pk])
    return format_html('<a href="{}">{}</a>', link, obj.product.title)

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
  list_display = ['id', 'user', 'product']
  def products(self, obj):
    link = reverse("admin:app_product_change", args=[obj.product.pk])
    return format_html('<a href="{}">{}</a>', link, obj.product.title)
  
@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'total_cost']
    list_filter = ['status', 'ordered_date']
    search_fields = ['user__username', 'customer__name', 'product__title']
    readonly_fields = ['ordered_date', 'total_cost']

    def total_cost(self, obj):
        return obj.total_cost

    total_cost.short_description = 'Total Cost'

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')

admin.site.register(Review, ReviewAdmin)

admin.site.unregister(Group)