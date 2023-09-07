from rest_framework import serializers 
from .models import *
from userapp.models import Dealer,User
# from userapp.serializer import UserSerializer

class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=image
        fields='__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category  # Corrected 'model' attribute, not 'models'
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

class VariantSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True ,source='image_set')
    class Meta:
        model=Variant
        fields='__all__'
        
class BrandGetSerializer(serializers.ModelSerializer):
    category=CategorySerializer()
    
    
    class Meta:
        model = Brand  # Corrected 'model' attribute, not 'models'
        fields ='__all__'



class VehicleSerializer(serializers.ModelSerializer):
    brand=BrandGetSerializer()
    Variant = VariantSerializer(many=True, read_only=True ,source='variant_set')
    images = ImageSerializer(many=True, read_only=True ,source='image_set')
    class Meta:
        model = Vehicle  # Corrected 'model' attribute, not 'models'
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    dealer = serializers.SerializerMethodField()
    vehicles = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = '__all__'

    def get_dealer(self, obj):
        dealers = Dealer.objects.filter(brand=obj)
        dealer_data = []

        for dealer in dealers:
            user_data = UserSerializer(dealer.user).data if dealer.user else None
            dealer_data.append({
                'dealer_info': DealerSerializer(dealer).data,
                'user_info': user_data
            })

        return dealer_data

    def get_vehicles(self, obj):
        vehicles = Vehicle.objects.filter(brand=obj)
        return VehicleSerializer(vehicles, many=True).data



class DealerSerializer(serializers.ModelSerializer):
    # brand=BrandSerializer()
    class Meta:
        model = Dealer
        fields = '__all__'   


class TestRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = testride
        fields = '__all__'



