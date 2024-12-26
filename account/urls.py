from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('register-supervisor/', views.SuperVisorRegister.as_view(), name='register-supervisor'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('forget-password/', views.ForgetPassword.as_view(), name='forget-password'),
    path('confirm-code/', views.ConfirmCode.as_view(), name='confirm-code'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify_otp'),
    path('<str:phone>/supervisor-dashboard/', views.supervisor_dashboard, name='supervisor-dashboard'),
    path('<str:phone>/dashboard/', views.dashboard, name='dashboard'),

]
