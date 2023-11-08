from django.db import models
from django.contrib.auth.models import User


def avatar_image_directory_path(instance: "ProfileUser", filename: str):
    return f"profile/profile_{instance.pk}/avatar/{filename}"


class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Имя")
    surname = models.CharField(max_length=200, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=200, verbose_name="Отчество")
    phone = models.CharField(max_length=15, verbose_name="Номер телефона")
    email = models.CharField(max_length=200, verbose_name="Email")
    avatar = models.ImageField(null=True, blank=True,
                               upload_to=avatar_image_directory_path)

    def get_avatar(self):
        avatar = {"src": self.avatar.url}
        return avatar

    def __str__(self):
        return self.name
