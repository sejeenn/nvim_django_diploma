from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.Serializer):
    class Meta:
        model = Profile
        fields = '__all__'

    def to_representation(self, instance):
        data = {
            "fullName": f"{instance.surname} {instance.name} {instance.patronymic}",
            "email": instance.user.email,
            "phone": instance.phone,
            "avatar": instance.get_avatar(),
        }
        return data
