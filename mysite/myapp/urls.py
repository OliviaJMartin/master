from django.urls import path
from . import views

urlpatterns = [
    path('', views.Overview.as_view(), name='overview'),
    path('overview/', views.Overview.as_view(), name='overview'),
    path('login/<machine>/', views.LoggingIn.as_view(), name='login'),
    path('login/', views.Overview.as_view(), name='overview'),
    path('logout/', views.LoggingOut.as_view(), name='logout'),
    path('machinestatus/', views.Status.as_view(), name='machineStatus'),
    path('updatestatus/', views.Update.as_view(), name='updateStatus'),
]