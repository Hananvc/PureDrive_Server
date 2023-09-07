from rest_framework.serializers import ModelSerializer,ValidationError
from .models import User,Dealer
from rest_framework import serializers
from vehicleapp.models import Brand
from vehicleapp.serializer import BrandSerializer

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
    brand=BrandSerializer()
    class Meta:
        model = Dealer
        fields = '__all__'    
        
class DealerCreateSerializer(serializers.ModelSerializer):
    # brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    # brand = BrandSerializer()  # Nested serializer for read operations
    # brand_id = serializers.IntegerField(write_only=True)  # brand_id for write operations
    class Meta:
        model = Dealer
        fields = [
            'user',
            'brand', 
            'address',
            'district',
            'website',
            'state',
            'pin_code',
            'country',
            'field_experience',
            'num_staff',
            'sales_contact_no',
            'service_contact_no',
            
        ]
        # extra_kwargs = {
        #     'password': {'write_only': True},
        # }

    def create(self, validated_data):
        DISTRICT_CHOICES = Dealer.DISTRICT_CHOICES
        STATE_CHOICES = Dealer.STATE_CHOICES
        COUNTRY_CHOICES = Dealer.COUNTRY_CHOICES

        district = serializers.ChoiceField(choices=DISTRICT_CHOICES)
        state = serializers.ChoiceField(choices=STATE_CHOICES)
        country = serializers.ChoiceField(choices=COUNTRY_CHOICES, default='india')
        # password = validated_data.pop('password')
        dealer = Dealer(**validated_data)
        # dealer.set_password(password)
        dealer.save()
        return dealer
    