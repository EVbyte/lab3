from django.urls import path, include
# from django.views.generic import ListView,DetailView
from .models import Articles
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from . import views


urlpatterns = [
    path('', ListView.as_view(queryset=Articles.objects.all().order_by("-date")[:20], template_name="news/post.html"), name='news_page'),
    path('<int:pk>/', views.HomeDetailView.as_view(), name='detail_page'),
    path('edit-page/', views.ArticleCreateView.as_view(), name='edit_page'),
    path('update-page/<int:pk>/', views.ArticleUpdateView.as_view(), name='update_page'),
    path('delete-page/<int:pk>/', views.ArticleDeleteView.as_view(), name='delete_page'),
    path('login-page/', views.FishingLoginView.as_view(), name='login_page'),
    path('register-page/', views.FishingRegisterView.as_view(), name='register_page'),
    path('logout/', views.FishingLogoutView.as_view(), name='logout_page'),
]
