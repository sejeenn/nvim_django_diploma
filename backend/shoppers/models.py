from django.db import models
from django.contrib.auth.models import User


def avatar_directory_path(instance: "Shopper", filename: str) -> str:
    return "shoppers/shopper_{pk}/avatar_img/{filename}".format(
            pk=instance.pk, filename=filename
            )

class Shopper(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, verbose_name="Имя")
    middle_name = models.CharField(max_length=200, verbose_name="Отчество")
    last_name = models.CharField(max_length=200, verbose_name="Фамилия")
    email = models.CharField(max_length=200, verbose_name="Электронная почта")
    phone = models.CharField(max_length=15, verbose_name="Номер телефона")
    avatar = models.ImageField(
            null=True,
            blank=True,
            upload_to=avatar_directory_path,
            )
    def get_avatar(self):
        avatar = {
                "src": self.avatar.url,
                "alt": self.avatar.name,
                }
        return avatar

    def __str__(self):
        return self.name
