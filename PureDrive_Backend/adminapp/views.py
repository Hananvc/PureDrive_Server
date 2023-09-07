from django.shortcuts import render
from vehicleapp.models import testride
from rest_framework import viewsets
from .serializer import *
from django.http import JsonResponse
from userapp.models import Dealer,User
from vehicleapp.models import News  # Import the custom User model from userapp
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Count, Case, When, Value
from rest_framework.parsers import MultiPartParser, FormParser





# Create your views here.
class TestRideListView(ReadOnlyModelViewSet):
    queryset = testride.objects.all()
    serializer_class = TestRideSerializer

    @action(detail=False, methods=['GET'])
    def testride_count(self, request):
        testride_counts = testride.objects.aggregate(
            total_testrides=Count('id'),
            completed_testrides=Count(
                Case(When(booking_status='Completed', then=Value(1)))
            ),
            cancelled_testrides=Count(
                Case(When(booking_status='Cancelled', then=Value(1)))
            ),
            pending_testrides=Count(
                Case(When(booking_status='Pending', then=Value(1)))
            ),
        )
        
        return Response(testride_counts)





class userView(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update','retrieve']:
            return [IsAuthenticated()]
        elif self.action == 'create':
            return [IsAdminUser()]
        else:
            return [IsAdminUser()]

    @action(detail=False, methods=['GET'])
    def user_count(self, request):
        user_count = User.objects.filter(is_dealer=False).count()
        return Response({'user_count': user_count})
    
    @action(detail=False, methods=['GET'])
    def dealer_count(self, request):
        dealer_count = Dealer.objects.count()
        return Response({'dealer_count': dealer_count})

    @action(detail=True, methods=['POST'])
    def block(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'message': 'User has been blocked'})

    @action(detail=True, methods=['POST'])
    def unblock(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'message': 'User has been unblocked'})


class dealerView(viewsets.ModelViewSet):
    queryset = Dealer.objects.select_related('user')
    serializer_class=DealerSerializer

    @action(detail=True, methods=['POST'])
    def block(self, request, pk=None):
        dealer = self.get_object()
        dealer.user.is_active = False
        dealer.user.save()
        return Response({'message': 'Dealer has been blocked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def unblock(self, request, pk=None):
        dealer = self.get_object()
        dealer.user.is_active = True
        dealer.user.save()
        return Response({'message': 'Dealer has been unblocked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def verify(self, request, pk=None):
        dealer = self.get_object()
        dealer.user.is_staff = True
        dealer.user.is_dealer = True
        dealer.user.save()
        return Response({'message': 'Dealer has been verified'}, status=status.HTTP_200_OK)


class newsView(viewsets.ModelViewSet):
    queryset=News.objects.all()
    serializer_class=NewsSerializer

class Brandview(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create_brand(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    parser_classes = [MultiPartParser, FormParser]  # Allow file uploads

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
    # Access the vehicle_id from request query parameters
        vehicle_id = request.query_params.get('vehicle_id')
        print(request.data, "data is")

        # Check if vehicle_id is provided and valid
        if not vehicle_id:
            return Response({'error': 'vehicle_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the vehicle instance using the provided vehicle_id
            vehicle = Vehicle.objects.get(pk=vehicle_id)
        except Vehicle.DoesNotExist:
            return Response({'error': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create a mutable copy of the request data
        mutable_data = request.data.copy()

        # Get the list of uploaded image files
        images = request.FILES.getlist('images')

        


        # Create an Image object for each uploaded image and associate it with the vehicle
        for image_file in images:
            mutable_data['Vehicle'] = vehicle.id
            mutable_data['images'] = image_file  # Assign the image file to the 'images' field

            # Serialize the data including the vehicle reference
            serializer = ImageSerializer(data=mutable_data)

            if serializer.is_valid():
                serializer.save()  # This will handle saving the image

        return Response({'message': 'Images saved successfully'}, status=status.HTTP_201_CREATED)




# Variant Viewset
class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer

    

class VariantViewSetnew(viewsets.ModelViewSet):
    queryset = Variant.objects.all()
    serializer_class = CreateVariantSerializer

    def create(self, request, *args, **kwargs):
        print("let me see the data",request.data)
        # Deserialize the request data using the serializer
        serializer = self.get_serializer(data=request.data)

        # Validate the data
        if serializer.is_valid():
            # Save the new Variant instance
            serializer.save()

            # Return a success response
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If the data is not valid, return an error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)