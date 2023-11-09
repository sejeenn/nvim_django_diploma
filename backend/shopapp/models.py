from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(models.Model):
    class Meta:
        ordering = ['title', 'price']
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    title = models.CharField(max_length=200, verbose_name="Название продукта")
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    count = models.IntegerField(default=0)
    description = models.TextField(null=False, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    def __str__(self):
        return self.title
