from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path("jwt-token", obtain_jwt_token),  # 通过此接口获取包含用户名和密码的令牌
    path('api/user/', include('apps.user.urls')),
    path('api/plan/', include('apps.plan.urls')),
    path('api/diary/', include('apps.diary.urls')),
    path('api/statistics/', include('apps.data_statistics.urls')),
    path('api/summary/', include('apps.summary.urls')),
]
