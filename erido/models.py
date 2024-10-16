from django.db import models
# from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.core.validators import MaxValueValidator
import uuid
from django.db.models import CheckConstraint, Q
from datetime import timedelta

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # username = models.CharField(max_length=100, null=False, unique=True)
    email = models.EmailField(null=False, unique=True)
    password = models.CharField(max_length=100, null=False)
    # first_name = models.CharField(max_length=100, null=False)
    # last_name = models.CharField(max_length=100, null=False)
    # verification_token = models.UUIDField(null=True, default=uuid.uuid4, blank=True)
    password_reset_token = models.UUIDField(null=True, blank=True)
    # is_verified = models.BooleanField(default=False)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return self.email
    
    def to_dict(self, request=None):
        return {
            'id': str(self.id),
            #'username': self.username,
            'email': self.email,
            #'first_name': self.first_name,
            #'last_name': self.last_name,
            #'verification_token': str(self.verification_token) if self.verification_token else None,
            'password_reset_token': str(self.password_reset_token) if self.password_reset_token else None,
            #'is_verified': self.is_verified,
        }

class MainCategory(models.Model):

    main_category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def to_dict(self, request=None):
        return {
            'main_category_id': self.main_category_id,
            'name': self.name,
        }

class SubCategory(models.Model):

    sub_category_id = models.AutoField(primary_key=True)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    def to_dict(self, request=None):
        return {
            'sub_category_id': self.sub_category_id,
            'main_category_id': self.main_category_id,
            'main_category_name': self.main_category.name,  # Assuming MainCategory has a 'name' field
            'name': self.name
        }

class Brand(models.Model):

    brand_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    def to_dict(self, request=None):
        return {
            'brand_id': self.brand_id,
            'name': self.name
        }

class Product(models.Model):

    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, unique=True, db_index=True)
    description = models.TextField(null=False)
    # ingredients = models.TextField(null=False)
    price = models.PositiveIntegerField(null=False, db_index=True)
    discount = models.PositiveIntegerField(default=0,null=False)
    discounted_price = models.PositiveIntegerField(null=False, editable=False)
    quantity_in_stock = models.PositiveIntegerField(null=False, db_index=True)
    subcategories = models.ManyToManyField(SubCategory)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    best_seller  = models.BooleanField(default=False, db_index=True)
    # image = models.TextField(null=False)
    image1 = models.ImageField(upload_to='images/', null=True, blank=True)
    image2 = models.ImageField(upload_to='images/', null=True, blank=True)
    image3 = models.ImageField(upload_to='images/', null=True, blank=True)
    image4 = models.ImageField(upload_to='images/', null=True, blank=True)
    slug = models.SlugField(default="", null=False, max_length=255, db_index=True)

    def __str__(self):
        return f'{self.name} - {self.price}'

    def to_dict(self, request=None):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'description': self.description,
            # 'ingredients': self.ingredients,
            'price': self.price,
            'discount': self.discount,
            'discounted_price': self.discounted_price,
            'quantity_in_stock': self.quantity_in_stock,
            # 'subcategories': [subcategory.to_dict() for subcategory in self.subcategories.all()],
            'best_seller': self.best_seller,
            'image1': self.image1.url if self.image1 else None,  # Convert to URL
            'image2': self.image2.url if self.image2 else None,  # Convert to URL
            'image3': self.image3.url if self.image3 else None,  # Convert to URL
            'image4': self.image4.url if self.image4 else None,  # Convert to URL
            'slug': self.slug,
            #'image1': self.image1,
            #'image2': self.image2,
            #'image3': self.image3,
            #'image4': self.image4,
            'brand': self.brand.name
        }
    
    class Meta:
        indexes = [
            models.Index(fields=['name', 'price', 'quantity_in_stock', 'best_seller', 'slug']),
        ]

    def save(self, *args, **kwargs):
        # Calculate the discounted price
        self.discounted_price = self.price * (100 - self.discount) / 100
        super().save(*args, **kwargs)

class ShoppingCart(models.Model):

    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart ID: {self.cart_id} - User: {self.user}'

    def to_dict(self, request=None):
        return {
            'cart_id': self.cart_id,
            'user': self.user.id if self.user else None,
            'session_key': self.session_key,
            'created_at': str(self.created_at),
        }

class CartItem(models.Model):

    item_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'Item ID: {self.item_id} - Product: {self.product.name} - Quantity: {self.quantity}'

    def to_dict(self, request=None):
        product_price = self.product.discounted_price if self.product.discount != 0 else self.product.price

        return {
            'product_id': self.product.product_id if self.product else None,
            'product_image': self.product.image1.url if self.product else None,
            # 'cart': self.cart.to_dict() if self.cart else None,
            'product_slug': self.product.slug if self.product else None,
            'product_name': self.product.name if self.product else None,
            'product_price': product_price,
            'quantity_in_stock': self.product.quantity_in_stock if self.product else None,
            'subtotal': product_price * self.quantity,
            'quantity': self.quantity,
        }

class Order(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Payment Completed', 'Payment Completed'),
        ('Delivered', 'Delivered'),
    ]

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.PositiveIntegerField()
    order_status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order ID: {self.order_id} - User: {self.user.email} - Status: {self.order_status}'

    def to_dict(self, request=None):
        return {
            'order_id': str(self.order_id),
            'user': str(self.user.id) if self.user else None,
            'total_amount': str(self.total_amount),
            'order_status': self.order_status,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

class OrderItem(models.Model):

    item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()

    def __str__(self):
        return f'Item ID: {self.item_id} - Product: {self.product.name} - Order: {self.order.order_id}'


    def to_dict(self, request=None):
        return {
            'order_item_id': self.item_id,
            'order': str(self.order.order_id), # Assuming you want to include the order ID
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'unit_price': self.unit_price
        }

class Review(models.Model):

    review_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    full_name = models.CharField(max_length=255)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review ID: {self.review_id} - Product: {self.product.name} - User: {self.user.email}'

    def to_dict(self, request=None):
        return {
            'review_id': self.review_id,
            'product': self.product.to_dict() if self.product else None,
            'user': self.user.email,
            'rating': self.rating,
            'comment': self.comment,
            'full_name': self.full_name,
            'created_at': self.created_at.strftime('%Y-%m-%d'),
        }

class Address(models.Model):

    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, null=True)
    street_address = models.CharField(max_length=255, null=True)
    town = models.CharField(max_length=255, null=True)
    county = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    additional_details = models.CharField(max_length=500, null=True)


    def __str__(self):
        return f'Address ID: {self.address_id} - User: {self.user.email}'

    def to_dict(self, request=None):
        return {
            'address_id': self.address_id,
            'user': self.user.email if self.user else None,
            'full_name': self.full_name,
            'street_address': self.street_address,
            'town': self.town,
            'county': self.county,
            'phone_number': self.phone_number,
            'additional_details': self.additional_details
        }

class Towns(models.Model):

    town_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    delivery_fee = models.PositiveIntegerField()

    def to_dict(self, request=None):
        return {
            'town_id': self.town_id,
            'name': self.name,
            'delivery_fee': self.delivery_fee,
        }

    def __str__(self):
        return f"Town ID: {self.town_id}, Name: {self.name}, Delivery Fee: {self.delivery_fee}"

class Wishlist(models.Model):
    wishlist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Wishlist ID: {self.wishlist_id} - User: {self.user.email} - Product: {self.product.name}'

    def to_dict(self, request=None):
        return {
            # 'wishlist_id': self.wishlist_id,
            # 'user': self.user.email,
            'product_slug': self.product.slug,
            'product_id': self.product.product_id if self.product else None,
            'product_image': self.product.image1.url if self.product else None,
            # 'cart': self.cart.to_dict() if self.cart else None,
            'product_name': self.product.name if self.product else None,
            'product_price': self.product.price if self.product else None,
            # 'product_discount': self.product.discount if self.product else None,
            'product_brand': self.product.brand.name if self.product else None,
            'product_quantity_in_stock': self.product.quantity_in_stock if self.product else None,
            # 'added_at': self.added_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Coupon(code={self.code}, discount={self.discount}%)"

    def to_dict(self):
        return {
            "code": self.code,
            "discount": float(self.discount),  # Convert Decimal to float for JSON serialization
            "active": self.active,
            "order_id": self.order.id if self.order else None
        }

class Maillist(models.Model):
    email = models.EmailField(null=False, unique=True)
    phone_number = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"Email: {self.email}, Phone Number: {self.phone_number}"

    def to_dict(self):
        return {
            'email': self.email,
            'phone_number': self.phone_number,
        }
