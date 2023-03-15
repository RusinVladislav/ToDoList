from django.urls import path

from todolist.core.views import SingUpView, LoginView, ProfileView, UpdatePasswordView

urlpatterns = [
    path('singup/', SingUpView.as_view(), name='singup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update_password/', UpdatePasswordView.as_view(), name='update_password'),
]
