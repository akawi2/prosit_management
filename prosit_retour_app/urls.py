from django.urls import path
from prosit_retour_app import views
from prosit_retour_app import download_retour 

urlpatterns = [
    path('home/', views.index, name='home'),
    path('download_retour/', download_retour.downloadRetour, name='downloadRetour')

]