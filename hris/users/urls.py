from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', LoginView.as_view(template_name='login.html', next_page='index'), name='login'),
]