
from AdminApp import views
from django.urls import path

urlpatterns = [
    path('',views.index),
    path('AdminAction', views.AdminAction),
    path('home', views.home),
    path('AddStations', views.AddStations),
    path('AddStationAction', views.AddStationAction),
    path('ViewStations',views.ViewStations),
    path('ViewEnergyDemand',views.ViewEnergyDemand),
    path('TimeWiseDemand', views.TimeWiseDemand),
    path('AmountWiseDemand',views.AmountWiseDemand),

]
