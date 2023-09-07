from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from vehicleapp.models import testride,News,Brand,Category,Vehicle,Variant,image
from userapp.models import User
from userapp.models import Dealer
from django.core.exceptions import ValidationError




class TestRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = testride
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    # ... other fields ...

    class Meta:
        model = Brand
        fields = '__all__'




class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = image
        fields = '__all__'
        extra_kwargs = {'images': {'required': True}}

class VehicleSerializer(serializers.ModelSerializer):
    # Use PrimaryKeyRelatedField or SlugRelatedField for updating the brand field
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())  # or SlugRelatedField
    images = ImageSerializer(many=True, read_only=True ,source='image_set')  # Add this line to include images

    class Meta:
        model = Vehicle
        fields = '__all__'

class VariantSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer()

    class Meta:
        model = Variant
        fields = '__all__'


class CreateVariantSerializer(serializers.ModelSerializer):
    # Include 'vehicle' as a writable field to accept data from the frontend
    vehicle = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all())

    class Meta:
        model = Variant
        fields = '__all__'





class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'username', 
            'phone', 
            'profile_image',
            'is_staff',
            'is_admin',
            'is_active',
            'is_dealer',
            ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.is_active = True
        user.set_password(password)
        user.save()
        print(user,'==================ser=============================')
        return user
    
    def validate(self, data):
     # For PATCH request, ensure users can only update their own data
        if self.context['request'].method == 'PATCH':
            if 'profile_picture' in data or 'number' in data:
                user = self.context['request'].user
                if user.id != self.instance.id:
                    raise ValidationError("You are not allowed to update these fields.")
       
        return data

class DealerSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    class Meta:
        model = Dealer
        fields = '__all__'