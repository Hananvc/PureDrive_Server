from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.http import JsonResponse
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from userapp.serializer import UserSerializer,DealerCreateSerializer,DealerSerializer
from userapp.utilities import create_otp
from .models import Dealer,User
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.decorators import action





User = get_user_model()




class SignUpView(CreateAPIView):
    def post(self, request,*args, **kwargs):
        serializer = UserSerializer(data=request.data)
        print(serializer,'=======================DATA----------------')
        serializer.is_valid()
        user=serializer.save()
        refresh=RefreshToken.for_user(user)
        data={
            'refresh':str(refresh),
            'access':str(refresh.access_token),
            'user':UserSerializer(user).data,
        }
        return Response(data,status=status.HTTP_201_CREATED)
    
class OtpView(CreateAPIView):
    permission_classes=[AllowAny]
    def post(self, request,*args, **kwargs):
        user = {
            'name': str(request.data['username']),
            'email': str(request.data['email'])
        }

        otp=create_otp(user)

        data={
            'user':request.data,
            'otp':otp   
        }

        return Response(data,status=status.HTTP_201_CREATED)

# class AuthView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         token = response.data['access']
#         response.data['token'] = token
#         response.data.pop('access', None)
#         response.data.pop('refresh', None)
#         email = request.data.get('email')
#         user = User.objects.get(email=email)
#         response.data['user'] = {
#             "name" : user.username,
#             "email" : user.email,
#             "user_id": user.id, 
#         }
#         print(response.data['user'],'==============================data=================')
#         return response

class AuthView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        role=request.data.get("role")
        
        if email and password and role:
            try:
                if role=="admin":
                    user=User.objects.get(email=email , is_admin=True)
                elif role=="dealer":
                    user=User.objects.get(email=email,is_dealer=True)
                else :
                    user=User.objects.get(email=email)
            except User.DoesNotExist:
               return Response({'message': 'User does not exist or is not authorized as {}.'.format(role)}, status=status.HTTP_404_NOT_FOUND) 
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                data={
                    'message': 'LOGIND',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user':UserSerializer(user).data,
                    'admin':user.is_admin,
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid credentials or not authorized to log in as {}.'.format(role)}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'message': 'Email and password is required.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def User_data(request, id):
    user = User.objects.get(id=id)
    # dealer = Dealer.objects.get(user=user)
    data = {
        'username': user.username,
        'email': user.email,
        'phone': user.phone,        
        'profile_image': user.profile_image,
        # Include other user data
    }
    serializer = UserSerializer(data)
    return Response(serializer.data)

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

        
class DealerViewSet(viewsets.ModelViewSet):
        queryset = Dealer.objects.all()
        serializer_class = DealerSerializer


            

class DealerRegistrationView(CreateAPIView):
    queryset = Dealer.objects.all()
    serializer_class = DealerCreateSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        userserializer = UserSerializer(data=request.data,context={'request': request})
        userserializer.is_valid(raise_exception=True)
        user=userserializer.save()
        user.save()
        print('ooooooooooooooooooooooooooooooooooooo')
        request.data['user']=user.id
        refresh=RefreshToken.for_user(user)
        print("cccccccccccccccccccccccccccccccccccccccccc")
        serializer = self.get_serializer(data=request.data)
        print(serializer,"FGVHJKLWERTYUYTREWQWERRYTUYR")
        print("pppppppppppppppppppppppppppppppppppppppp")
        serializer.is_valid(raise_exception=True)
        print(serializer.errors,"&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
        dealer = serializer.save()  # Use serializer.save() to call custom create method in serializer
        data = {
            'refresh':str(refresh),
            'access':str(refresh.access_token),
            "message": "Dealer registered successfully.",
            "user": DealerCreateSerializer(dealer).data
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Provide the choices for 'district', 'state', and 'country' fields to the serializer context
        context['district_choices'] = Dealer.DISTRICT_CHOICES
        context['state_choices'] = Dealer.STATE_CHOICES
        context['country_choices'] = Dealer.COUNTRY_CHOICES
        return context




class SignUpView(CreateAPIView):
    def post(self, request,*args, **kwargs):
        serializer = UserSerializer(data=request.data,context={'request': request})
        # print(serializer,'=======================DATA----------------')
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        refresh=RefreshToken.for_user(user)
        data={
            'refresh':str(refresh),
            'access':str(refresh.access_token),
            'user':UserSerializer(user).data,
        }
        return Response(data,status=status.HTTP_201_CREATED)

class ObtainNewAccessToken(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh_token = RefreshToken(refresh_token)
            access_token = str(refresh_token.access_token)
            return Response({"access_token": access_token}, status=status.HTTP_200_OK)

        except:
            return Response({"error": "Invalid refresh token."}, status=status.HTTP_401_UNAUTHORIZED)