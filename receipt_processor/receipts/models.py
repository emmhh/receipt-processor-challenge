from django.db import models
import uuid
import math
from datetime import time

class Receipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    retailer = models.CharField(max_length=255)
    purchase_date = models.DateField()
    purchase_time = models.TimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    points = models.IntegerField(default=0)

    def calculate_points(self):
        points = 0
        
        # One point for every alphanumeric character in the retailer name
        points += sum(c.isalnum() for c in self.retailer)
        
        # 50 points if the total is a round dollar amount with no cents
        if float(self.total) % 1 == 0:
            points += 50
            
        # 25 points if the total is a multiple of 0.25
        if float(self.total) % 0.25 == 0:
            points += 25
            
        # 5 points for every two items on the receipt
        items_count = self.items.count()
        points += (items_count // 2) * 5
        
        # Points for items with description length multiple of 3
        for item in self.items.all():
            desc_length = len(item.short_description.strip())
            if desc_length % 3 == 0:
                points += math.ceil(float(item.price) * 0.2)
        
        # 6 points if the day in the purchase date is odd
        if self.purchase_date.day % 2 == 1:
            points += 6
            
        # 10 points if the time of purchase is after 2:00pm and before 4:00pm
        purchase_time = self.purchase_time
        if time(14, 0) <= purchase_time <= time(16, 0):
            points += 10
            
        return points

    def save(self, *args, **kwargs):
        self.points = self.calculate_points()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.retailer} - {self.purchase_date}"

class Item(models.Model):
    receipt = models.ForeignKey(Receipt, related_name='items', on_delete=models.CASCADE)
    short_description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.short_description