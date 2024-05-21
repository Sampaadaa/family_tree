from django.urls import path
from .views import family_tree 

urlpatterns = [
    path('tree/',family_tree),
]
