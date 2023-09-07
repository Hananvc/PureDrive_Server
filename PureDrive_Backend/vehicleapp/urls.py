from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'vehicle', VehicleView)
router.register(r'brand', Brandview)
router.register(r'category', CategoryView)
router.register(r'variant', VariantView)
router.register(r'image', ImageView)
router.register(r'testride', TestRideListView) 





urlpatterns = [
    path('brands/', get_brands, name='brands-list'),
    #  path('alldata/', AllDataView.as_view(), name='alldata'),
    # Other URL patterns for your application
    path('',include(router.urls)),
    path('cached-news/', CachedNewsListView.as_view(), name='cached-news-list'),
    path('fetch-initial-news/', FetchAndStoreInitialNews.as_view(), name='fetch-initial-news'),
    path('book-testride/', TestRideBookingView.as_view(), name='book-testride'),
    path('user-bookings/', UserBookingsView.as_view(), name='user-bookings'),
    path('dealer-bookings/', DealerBookingsView.as_view(), name='dealer-bookings'),
    path('testride-cancel/<int:pk>/', TestRideCancellationView.as_view(), name='testride-cancel'),
    path('change-booking-status/<int:pk>/', BookingStatusChangeView.as_view(), name='change-booking-status'),
]
