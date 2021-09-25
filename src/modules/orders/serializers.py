from .models import Order
from rest_framework import serializers

class SerializedOrder(serializers.ModelSerializer):
    items = serializers.JSONField()

    class Meta:
        model = Order
        fields = ('id', 'items', 'total')