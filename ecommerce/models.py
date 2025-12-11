from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError


# ============================
# CATEGORY MODEL
# ============================
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]
        app_label = "ecommerce"  # Ensure correct app 
        db_table = "ecommerce_category"  # Custom table name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate a unique slug if not provided"""
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            i = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("ecommerce:category_products", args=[self.slug])


# ============================
# PRODUCT MODEL
# ============================
class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, db_index=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["category", "available"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug, manage availability, and check stock"""
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            i = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{i}"
                i += 1
            self.slug = slug

        # Automatically mark unavailable if stock = 0
        self.available = self.stock > 0

        super().save(*args, **kwargs)

        # Send low-stock alert after saving
        self.check_stock()

    def clean(self):
        """Validate that available products must have stock"""
        super().clean()
        if self.available and self.stock == 0:
            raise ValidationError({
                "available": "Product cannot be marked as available when stock is 0."
            })

    def get_absolute_url(self):
        return reverse("ecommerce:product_detail", args=[self.slug])

    @property
    def is_in_stock(self):
        """Check if product is both available and has stock"""
        return self.available and self.stock > 0

    @property
    def display_price(self):
        """Formatted price for templates"""
        return f"Rs {self.price:.2f}"

    def check_stock(self):
        """Send email alert if stock <= 10"""
        if self.stock <= 10:
            send_mail(
                subject=f"⚠️ Low Stock Alert: {self.name}",
                message=f"The product '{self.name}' has only {self.stock} left in stock. Please restock soon.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )


# ============================
# SALE MODEL
# ============================
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"

    def save(self, *args, **kwargs):
        """Auto-calculate total price and reduce product stock"""
        if not self.total_price:
            self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

        # Update product stock
        self.product.stock -= self.quantity
        self.product.save()


