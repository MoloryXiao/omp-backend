from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'user-info', views.UserInfoModelView)
urlpatterns = [
    path('', include(router.urls)),  # 默认路由
    path(r'user-register/', views.UserRegister.as_view())
]
