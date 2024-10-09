from django.contrib import admin
from .models import User, MainCategory, SubCategory, Brand, Product, ShoppingCart, CartItem, Order, OrderItem, Review, Address, Towns, Wishlist, Coupon, Maillist

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'password_reset_token')
    fields = ('id', 'email', 'password', 'password_reset_token')
    readonly_fields = ('id',)
    search_fields = ('email',)

class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('main_category_id', 'name')
    search_fields = ('name',)

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('sub_category_id', 'main_category', 'name')
    search_fields = ('name', 'main_category__name')
    list_filter = ('main_category',)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_id', 'name')
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'price', 'discount', 'discounted_price', 'quantity_in_stock', 'best_seller', 'brand')
    search_fields = ('name', 'brand__name')
    list_filter = ('best_seller', 'brand', 'subcategories')
    ordering = ('-price',)

class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'user', 'session_key', 'created_at')
    search_fields = ('user__email', 'session_key')
    list_filter = ('created_at',)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'cart', 'product', 'quantity')
    search_fields = ('cart__cart_id', 'product__name')
    list_filter = ('cart', 'product')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'total_amount', 'order_status', 'created_at')
    search_fields = ('user__email', 'order_id')
    list_filter = ('order_status', 'created_at')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'order', 'product', 'quantity', 'unit_price')
    search_fields = ('order__order_id', 'product__name')
    list_filter = ('order', 'product')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'product', 'user', 'rating', 'full_name', 'created_at')
    search_fields = ('product__name', 'user__email', 'full_name')
    list_filter = ('rating', 'created_at')

class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_id', 'user', 'full_name', 'street_address', 'town', 'county', 'phone_number')
    search_fields = ('user__email', 'full_name', 'town')
    list_filter = ('town', 'county')

class TownsAdmin(admin.ModelAdmin):
    list_display = ('town_id', 'name', 'delivery_fee')
    search_fields = ('name',)
    list_filter = ('delivery_fee',)

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('wishlist_id', 'user', 'product', 'added_at')
    search_fields = ('user__email', 'product__name')
    list_filter = ('added_at',)

class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'active', 'order')
    search_fields = ('code',)
    list_filter = ('active', 'order')

class MaillistAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number')
    search_fields = ('email', 'phone_number')

# Register your models with the admin site
admin.site.register(User, UserAdmin)
admin.site.register(MainCategory, MainCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Towns, TownsAdmin)
admin.site.register(Wishlist, WishlistAdmin)
# admin.site.register(Coupon, CouponAdmin)
# admin.site.register(Maillist, MaillistAdmin)
