from django.urls import path

from . import views

urlpatterns = [
    path("inbox/", views.inbox_endpoint, name="inbox"),
]
