from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserAuthView, UserTokenView, UserViewSet

app_name = 'users'

router = SimpleRouter()
router.register('users', UserViewSet)


urlpatterns = [
    path('auth/signup/', UserAuthView.as_view()),
    path('auth/token/', UserTokenView.as_view()),
    path('', include(router.urls)),
    path('users/me/', UserViewSet)
]
