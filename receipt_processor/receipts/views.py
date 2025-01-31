from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Receipt
from .serializers import ReceiptSerializer, ReceiptResponseSerializer, PointsResponseSerializer
from django.core.exceptions import ValidationError
import uuid

@api_view(['POST'])
def process_receipt(request):
    serializer = ReceiptSerializer(data=request.data)
    if serializer.is_valid():
        receipt = serializer.save()
        receipt.save()  # This will trigger points calculation
        response_serializer = ReceiptResponseSerializer(receipt)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    return Response(
        {"error": "Please verify input.", "details": serializer.errors}, 
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
def get_points(request, id):
    try:
        # First validate if the id is a valid UUID
        try:
            uuid_obj = uuid.UUID(id)
        except ValueError:
            return Response(
                {"error": "Invalid receipt id format"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        receipt = Receipt.objects.get(id=uuid_obj)
        return Response({"points": receipt.points})
    except Receipt.DoesNotExist:
        return Response(
            {"error": "No receipt found for that id"}, 
            status=status.HTTP_404_NOT_FOUND
        )