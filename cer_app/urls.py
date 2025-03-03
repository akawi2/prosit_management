from django.urls import path
from cer_app import views
from cer_app import download_cer

urlpatterns = [
    path('home/', views.index, name='home'),
    path('create_cer/', views.generateCER, name='create_cer'),
    path('create_ppt/', views.generateRetour, name='create_ppt'),
    path('presentation_cer/', views.cer_presentation, name='cer_presentation'),
    path('retour_presentation/', views.retour_presentation, name='retour_presentation'),
    path('download_cer/', download_cer.downloadCER, name='download_cer'),
]