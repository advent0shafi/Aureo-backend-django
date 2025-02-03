from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView,CustomTokenObtainPairView,UserDetailView,UserViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet)

# URL Patterns
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('users/', include(router.urls)),
]

