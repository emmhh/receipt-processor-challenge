from rest_framework import serializers
from .models import Receipt, Item

class ItemSerializer(serializers.ModelSerializer):
    shortDescription = serializers.CharField(source='short_description')

    class Meta:
        model = Item
        fields = ['shortDescription', 'price']

class ReceiptSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    purchaseDate = serializers.DateField(source='purchase_date')
    purchaseTime = serializers.TimeField(source='purchase_time')

    class Meta:
        model = Receipt
        fields = ['retailer', 'purchaseDate', 'purchaseTime', 'items', 'total']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        receipt = Receipt.objects.create(**validated_data)
        
        for item_data in items_data:
            Item.objects.create(receipt=receipt, **item_data)
        
        return receipt

class ReceiptResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['id']

class PointsResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['points']