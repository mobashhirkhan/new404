from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_nodes, name='get_all_nodes'),
    # path('<int:id>/', views.get_node, name='get_node'),
]