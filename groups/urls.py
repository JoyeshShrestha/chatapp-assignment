from django.urls import path

from .views import GroupView, addMembersView, UGView


urlpatterns = [
    path("", GroupView.as_view()),
    path("addmembers/", addMembersView.as_view()),
    path("viewgroup/", UGView.as_view()),


]
    