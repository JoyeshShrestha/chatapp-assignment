from django.urls import path

from .views import GroupView


urlpatterns = [
    path("", GroupView.as_view()),
]
    