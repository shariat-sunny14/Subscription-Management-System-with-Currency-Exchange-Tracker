from django.urls import path
from .views import register_view
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', CustomLoginView.as_view(), name='root_login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
