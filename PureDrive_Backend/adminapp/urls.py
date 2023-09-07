
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'testride', TestRideListView) 
router.register(r'user', userView)
router.register(r'dealer', dealerView)
router.register(r'news', newsView)
router.register(r'brand', Brandview)
router.register(r'vehicle', VehicleViewSet)
router.register(r'images', ImageViewSet) 
router.register(r'variants', VariantViewSet)
router.register(r'createvariant', VariantViewSetnew)







urlpatterns = [
    path('',include(router.urls)),
    # path('get_dealer_user_counts/', get_dealer_user_counts, name='get_dealer_user_counts'),

]
