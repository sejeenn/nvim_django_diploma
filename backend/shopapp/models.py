from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from myauth.models import ProfileUser


def category_image_directory_path(instance: "Category", filename: str):
    return f"categories/category_{instance.pk}/image/{filename}"


class Category(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(max_length=200, verbose_name="Категория товара")
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=category_image_directory_path
    )

    def get_image(self):
        image = {
            "src": self.image.url,
            "alt": self.image.name,
        }
        return image


def subcategory_image_directory_path(instance: "SubCategory", filename: str):
    return f"subcategories/subcategory_{instance.pk}/image/{filename}"


class SubCategory(models.Model):
    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    title = models.CharField(max_length=200, verbose_name="Подкатегория товара")
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=subcategory_image_directory_path
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        verbose_name="Подкатегория товара",
        null=True,
    )

    def get_image(self):
        image = {
            "src": self.image.url,
            "alt": self.image.name,
        }
        return image


def product_images_directory_path(instance: "Product", filename: str) -> str:
    return f"products/product_{instance.pk}/image/{filename}"


class Tag(models.Model):
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        ordering = ['title', 'price']
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    count = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    title = models.CharField(max_length=200, verbose_name="Название продукта")
    description = models.TextField(null=False, blank=True)
    specification = models.ManyToManyField(
        "Specification", verbose_name="Характеристика", related_name="products"
    )
    freeDelivery = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, verbose_name="Тег", related_name="tags")

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    def get_image(self):
        """
        Данный метод возвращает список словарей с адресами картинок продукта
        """
        images = ProductImage.objects.filter(product_id=self.pk)
        return [
            {"src": image.image.url, "alt": image.image.name} for image in images
        ]

    def get_rating(self):
        """Метод получения рейтинга продукта по количеству отзывов и их оценок"""
        reviews = Review.objects.filter(product_id=self.pk).values_list(
            "rate", flat=True
        )
        if reviews.count() == 0:
            rating = 0
            return rating
        rating = sum(reviews) / reviews.count()
        return rating

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to=product_images_directory_path)


class Review(models.Model):
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    author = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания отзыва")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        verbose_name="Товар", related_name="reviews"
    )
    rate = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5)], verbose_name="Оценка"
    )

    def __str__(self):
        return str(self.rate)


class Specification(models.Model):
    class Meta:
        verbose_name = "Спецификация"
        verbose_name_plural = "Спецификации"

    name = models.CharField(max_length=50, blank=True, null=True)
    value = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name}: {self.value}"
