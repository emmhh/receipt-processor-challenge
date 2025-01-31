from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Receipt, Item

class ReceiptAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_target_receipt_example(self):
        # First example from README
        receipt_data = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {
                    "shortDescription": "Mountain Dew 12PK",
                    "price": "6.49"
                },
                {
                    "shortDescription": "Emils Cheese Pizza",
                    "price": "12.25"
                },
                {
                    "shortDescription": "Knorr Creamy Chicken",
                    "price": "1.26"
                },
                {
                    "shortDescription": "Doritos Nacho Cheese",
                    "price": "3.35"
                },
                {
                    "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                    "price": "12.00"
                }
            ],
            "total": "35.35"
        }

        # Process receipt
        response = self.client.post(
            reverse('process_receipt'),
            receipt_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Get receipt ID from response
        receipt_id = response.data['id']
        
        # Check points
        points_response = self.client.get(
            reverse('get_points', args=[receipt_id])
        )
        self.assertEqual(points_response.status_code, status.HTTP_200_OK)
        self.assertEqual(points_response.data['points'], 28)

    def test_mm_corner_market_receipt_example(self):
        # Second example from README
        receipt_data = {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [
                {
                    "shortDescription": "Gatorade",
                    "price": "2.25"
                },
                {
                    "shortDescription": "Gatorade",
                    "price": "2.25"
                },
                {
                    "shortDescription": "Gatorade",
                    "price": "2.25"
                },
                {
                    "shortDescription": "Gatorade",
                    "price": "2.25"
                }
            ],
            "total": "9.00"
        }

        # Process receipt
        response = self.client.post(
            reverse('process_receipt'),
            receipt_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Get receipt ID from response
        receipt_id = response.data['id']
        
        # Check points
        points_response = self.client.get(
            reverse('get_points', args=[receipt_id])
        )
        self.assertEqual(points_response.status_code, status.HTTP_200_OK)
        self.assertEqual(points_response.data['points'], 109)

    def test_invalid_receipt_id(self):
        # Test invalid UUID format
        response = self.client.get('/receipts/invalid-uuid/points')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test non-existent but valid UUID format
        valid_uuid = '47d4275f-8bd6-4d3a-a51d-9c0c9f0c144e'
        response = self.client.get(f'/receipts/{valid_uuid}/points')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
