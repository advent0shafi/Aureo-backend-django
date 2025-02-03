from django.urls import path
from .views import CartAPIView

urlpatterns = [
    path('carts/', CartAPIView.as_view(), name='cart'),  # For GET and POST
    path('carts/<int:pk>/', CartAPIView.as_view(), name='cart-detail'),  # For PUT, PATCH, DELETE
]