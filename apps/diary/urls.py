from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'diaries', views.Diary)
urlpatterns = [
    path('', include(router.urls)),  # 默认路由
    path(r'detect/', views.DiaryHandler.as_view()),
]
