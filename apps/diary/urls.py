from django.urls import include, path
from . import views

urlpatterns = [
    path(r'detect/', views.DiaryHandler.as_view())
]
