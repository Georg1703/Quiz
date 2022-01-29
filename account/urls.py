from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers

from account.views import RegisterView, UserViewSet

router = routers.SimpleRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='register'),
    path('refresh-token/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
