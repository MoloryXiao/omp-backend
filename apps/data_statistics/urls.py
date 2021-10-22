from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'daily_time', views.DailyTimeCollect)
router.register(r'operation_records', views.OperationRecordModelView)
urlpatterns = [
    path('', include(router.urls)),  # 默认路由
]
