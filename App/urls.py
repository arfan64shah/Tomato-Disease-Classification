from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='main'),
	path('binaryClassification', views.binaryClassification, name='binaryClassification'),
    path('multiClassification', views.multiClassification, name='multiClassification'),
    path('predictBinary',views.predictBinary,name='predictBinary'),
    path('binaryResults',views.predictBinary,name='binaryResults'),
    path('predictMulti',views.predictMulti,name='predictMulti'),
    path('multiResults',views.predictMulti,name='multiResults'),
]