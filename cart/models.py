

from django.db import models
from django.conf import settings
from products.models import Product
from decimal import Decimal

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="cart")
    guest_id = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Guest Cart {self.guest_id}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def shipping_cost(self):
        return Decimal('0.00')  # Example: Free shipping

    @property
    def vat(self):
        VAT_RATE = Decimal('0.05')  # Convert to Decimal
        return self.subtotal * VAT_RATE

    @property
    def total(self):
        return self.subtotal + self.shipping_cost + self.vat

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    # Add more details from the Product if needed (make them read-only)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at the time of adding to cart
    currency = models.CharField(max_length=10)
    material = models.CharField(max_length=100, blank=True, null=True)
    diamond_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    diamond_quality = models.CharField(max_length=50, null=True, blank=True)
    sku = models.CharField(max_length=100)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name_en} in {self.cart}"

    @property
    def subtotal(self):
        """Calculates the subtotal for this cart item."""
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        """
        Override save to copy relevant details from the Product to the CartItem
        at the time of adding to the cart.
        """
        if not self.pk:  # Only on creation
            self.price = self.product.price
            self.currency = self.product.currency
            self.material = self.product.material
            self.diamond_weight = self.product.diamond_weight
            self.diamond_quality = self.product.diamond_quality
            self.sku = self.product.sku
        super().save(*args, **kwargs)