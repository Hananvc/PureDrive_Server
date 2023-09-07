from django.http import JsonResponse
from .models import *
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from .serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import News
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .tasks import fetch_and_store_news
import random
import string
from django.db.utils import IntegrityError



def get_brands(request):
    brands = Brand.objects.all()
    data = [{'id': brand.id, 'name': brand.name} for brand in brands]
    return JsonResponse(data, safe=False)




class VehicleView(viewsets.ModelViewSet):
    queryset=Vehicle.objects.all()
    serializer_class = VehicleSerializer

    # def get_permissions(self):
    #     if self.action in ['update', 'partial_update','retrieve']:
    #         return [IsAuthenticated()]
    #     elif self.action == 'create':
    #         return [IsAdminUser()]
    #     else:
    #         return [IsAdminUser()]

class CategoryView(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class = CategorySerializer

class VariantView(viewsets.ModelViewSet):
    queryset=Variant.objects.all()
    serializer_class = VariantSerializer

class Brandview(viewsets.ModelViewSet):
    queryset=Brand.objects.all()
    serializer_class = BrandSerializer

class ImageView(viewsets.ModelViewSet):
    queryset=image.objects.all()
    serializer_class = ImageSerializer



# class AllDataView(APIView):

#     def get(self, *args, **kwargs):
#         try :
#             variants = Variant.objects.all()
#             data = {}

#             for variant in variants:
#                 data[variant.id] = {
#                     'vehicles': Vehicle.objects.filter(id=variant.vehicle.id),
#                     'brand':Brand.objects.filter(id=variant.vehicle.brand.id),
#                     'category':Category.objects.filter(id=variant.vehicle.brand.category.id),
#                     'image':image.objects.filter(Variant=variant),
#                 }

#             # Serialize the data
#             valid_data = {}
#             for variant_id, value in data.items():
#                 valid_data[variant_id] = {
#                     'vehicles_data': VehicleSerializer(value['vehicles'], many=True).data,
#                     'brand':BrandSerializer(value['brand'], many=True).data,
#                     'category':CategorySerializer(value['category'],many=True).data,
#                     'image':ImageSerializer(value['image'],many=True).data,
#                 }
#         except:
#             pass


#         return Response(valid_data)
    # def get(self, request):
    #     # Fetch data from all the models
    #     categories = Category.objects.all()
    #     brands = Brand.objects.all()
    #     vehicles = Vehicle.objects.all()
    #     variants = Variant.objects.all()
    #     images = image.objects.all()

    #     # Serialize the data
    #     categories_data = CategorySerializer(categories, many=True).data
    #     brands_data = BrandSerializer(brands, many=True).data
    #     vehicles_data = VehicleSerializer(vehicles, many=True).data
    #     variants_data = VariantSerializer(variants, many=True).data
    #     images_data = ImageSerializer(images, many=True).data

    #     # Prepare the response data
    #     response_data = {
    #         'categories': categories_data,
    #         'brands': brands_data,
    #         'vehicles': vehicles_data,
    #         'variants': variants_data,
    #         'images': images_data,
    #     }

    #     return Response(response_data)


import requests
from rest_framework import status


class FetchAndStoreInitialNews(APIView):
    def post(self, request, format=None):
        try:
            # Replace 'YOUR_API_KEY' with your actual NewsAPI API key
            api_key = 'ca789e9ab879409488626410ac1186ad'
            api_url = f'https://newsapi.org/v2/everything?q=electric%20vehicle&apiKey={api_key}'
            response = requests.get(api_url)
            print(response)
            news_data = response.json().get('articles', [])

            if not news_data:
                print("API response does not contain news data. Skipping addition.")
                return Response({'message': 'API response does not contain news data.'})

            News.objects.all().delete()
            print("Cleared existing news data")

            news_added = 0
            max_news_count = 100

            for article in news_data:
                if news_added >= max_news_count:
                    print("Maximum news limit reached. Stopping further addition.")
                    break
                try:
                    News.objects.create(
                        title=article['title'],
                        description=article['description'],
                        url=article['url'],
                        url_to_image=article['urlToImage'],
                    )
                    news_added += 1
                except IntegrityError as e:
                    print('Error adding news article:', exc_info=True)
                    continue  # Skip this article and continue with the next
            
            
            return Response({'message': 'News data fetched and stored successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Error fetching and storing news data.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CachedNewsListView(APIView):
    def get(self, request, *args, **kwargs):
        # Check if cached news data exists and if it's less than 1 day old
        cache_time_threshold = datetime.now() - timedelta(days=1)
        cached_news = News.objects.all().order_by('-id')

        if cached_news.exists():
            serialized_news = [{'title': news.title, 'description': news.description, 'url': news.url, 'urlToImage': news.url_to_image} for news in cached_news]
            return Response(serialized_news)
        else:
            return Response({'message': 'No cached news data available.'}, status=204)  # No Content


class TestRideBookingView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data,'tttttttttttttttttttttttttttttttttttttttttttttt')
        booking_reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        dealer_mail = User.objects.get(username=data['dealer'])
        booking = testride.objects.create(
            booking_reference=booking_reference,
            brand=data['brand'],
            model_name=data['model_name'],
            date=data['date'],
            time=data['time'],
            dealer=data['dealer'],
            dealer_email=dealer_mail.email,
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            customer_phone=data['customer_phone']
        )
        print("BOOKED")
        return Response({"message": "Booking created successfully"}, status=status.HTTP_201_CREATED)
    
class UserBookingsView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user  # Assuming the user is logged in
        bookings = testride.objects.filter(customer_email=user.email)
        
        booking_data = []
        for booking in bookings:
            
            booking_data.append({
                "id" : booking.id,
                "booking_reference": booking.booking_reference,
                "brand": booking.brand,
                "model_name": booking.model_name,
                "date": booking.date,
                "time": booking.time,
                "dealer": booking.dealer,
                "booking_status": booking.booking_status,
                "review" : booking.review,
            })
        
        return Response(booking_data, status=status.HTTP_200_OK)
    
class DealerBookingsView(APIView):
    def get(self, request, *args, **kwargs):
        dealer = request.user  # Assuming the dealer is logged in
        bookings = testride.objects.filter(dealer_email=dealer.email)
        
        booking_data = []
        for booking in bookings:
            user = User.objects.get(email=booking.customer_email)
            booking_data.append({
                "id" : booking.id,
                "booking_reference": booking.booking_reference,
                "brand": booking.brand,
                "model_name": booking.model_name,
                "date": booking.date,
                "time": booking.time,
                "dealer": booking.dealer,
                "booking_status": booking.booking_status,
                "customer_name": user.username,
                "customer_email": user.email,
                "customer_phone" : user.phone,
                "review" : booking.review,

              
            })
        
        return Response(booking_data, status=status.HTTP_200_OK)

    
class TestRideCancellationView(APIView):
    def put(self, request, pk):
        try:
            ride = testride.objects.get(pk=pk)
        except testride.DoesNotExist:
            return Response({"message": "Test ride not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if ride.booking_status != "Pending":
            return Response({"message": "Cannot cancel a ride that is not pending"}, status=status.HTTP_400_BAD_REQUEST)
        
        ride.booking_status = "Cancelled"
        ride.save()
        
        return Response({"message": "Test ride cancelled successfully"}, status=status.HTTP_200_OK)
    

class BookingStatusChangeView(APIView):
    def put(self, request, pk):
        try:
            booking = testride.objects.get(pk=pk)
        except testride.DoesNotExist:
            return Response({"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        
        new_status = request.data.get('status')  # Assuming the status is sent in the request data
        
        # Add your own validation checks here if needed
        
        booking.booking_status = new_status
        booking.save()
        print("status changed succesfully")
        
        return Response({"message": f"Booking status changed to {new_status} successfully"}, status=status.HTTP_200_OK)
    
class TestRideListView(viewsets.ModelViewSet):
    queryset = testride.objects.all()
    serializer_class = TestRideSerializer