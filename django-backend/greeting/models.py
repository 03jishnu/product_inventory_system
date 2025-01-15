from django.db import models
from django.contrib.auth.models import User
from versatileimagefield.fields import VersatileImageField
import uuid
import decimal

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.BigIntegerField(unique=True)
    product_code = models.CharField(max_length=255, unique=True)
    product_name = models.CharField(max_length=255)
    product_image = VersatileImageField(upload_to="uploads/", blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    created_user = models.ForeignKey(User, related_name="user%(class)s_objects", on_delete=models.CASCADE)
    is_favourite = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    hsn_code = models.CharField(max_length=255, blank=True, null=True)
    total_stock = models.DecimalField(default=0.00, max_digits=20, decimal_places=8, blank=True, null=True)

    class Meta:
        db_table = "products_product"
        verbose_name = "product"
        verbose_name_plural = "products"
        unique_together = (("product_code", "product_id"),)
        ordering = ("-created_date", "product_id")

    def __str__(self):
        return self.product_name

    def calculate_total_stock(self):
        """Calculates the total stock for the product based on its variants and subvariants."""
        total_stock = decimal.Decimal(0)
        for variant in self.variants.all():
            total_stock += variant.calculate_total_stock()
            for subvariant in variant.subvariants.all():
                total_stock += subvariant.total_stock
        return total_stock

class Variant(models.Model):
    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    options = models.JSONField()  # This stores the options
    total_stock = models.DecimalField(default=0.00, max_digits=20, decimal_places=8, blank=True, null=True)

    def __str__(self):
        return self.name

    def calculate_total_stock(self):
        """Calculates the total stock for the variant based on its options."""
        total_stock = decimal.Decimal(0)
        for option in self.options:
            total_stock += decimal.Decimal(option.get('stock', 0))
        return total_stock

class SubVariant(models.Model):
    variant = models.ForeignKey(Variant, related_name="subvariants", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    option_name = models.JSONField()  
    total_stock = models.DecimalField(default=0.00, max_digits=20, decimal_places=8, blank=True, null=True)

    def __str__(self):
        return f"{self.variant.name} - {self.option_name}"

    def calculate_total_stock(self):
        """Calculates total stock for the subvariant by summing the stock of its options."""
        return decimal.Decimal(self.option_name.get('stock', 0))
