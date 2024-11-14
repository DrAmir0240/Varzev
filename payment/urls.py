from django.urls import path
from . import views

urlpatterns = [
    path('<int:session_id>/', views.reserve, name='reserve'),
    path('payment/<reserve_id>/', views.payment, name='payment'),
    path('delete/<int:reserve_id>/', views.delete, name="delete"),
    path('request/<int:reserve_id>/', views.send_request, name='request'),
    path('verify/', views.verify, name='verify'),

]