from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'month_plans', views.MonthPlan)
router.register(r'week_plans', views.WeekPlan)
urlpatterns = [
    path('', include(router.urls)),  # 默认路由
]
