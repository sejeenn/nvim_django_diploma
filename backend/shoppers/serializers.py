from rest_framework import serializers

from .models import Shopper


class ShopperSerializer(serializers.Serializer):
    class Meta:
        model = Shopper
        fields = '__all__'

    def to_representation(self, instance):
        data = {
            "fullName": f"{instance.last_name} {instance.first_name} {instance.middle_name}",
            "email": f"{instance.email}",
            "phone": f"{instance.phone}",
            "avatar": instance.get_avatar(),
        }
        return data
