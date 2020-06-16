from django.urls import path, include, re_path
# from django.views.generic import ListView,DetailView
from .models import Articles
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('', ListView.as_view(queryset=Articles.objects.all().order_by("-date")[:20], template_name="books/post.html",), name='news_page'),
    path('<int:pk>/', views.HomeDetailView.as_view(), name='detail_page'),
    path('edit-page/', views.ArticleCreateView.as_view(), name='edit_page'),
    path('update-page/<int:pk>/', views.ArticleUpdateView.as_view(), name='update_page'),
    path('delete-page/<int:pk>/', views.ArticleDeleteView.as_view(), name='delete_page'),
    path('login-page/', views.FishingLoginView.as_view(), name='login_page'),
    path('register-page/', views.FishingRegisterView.as_view(), name='register_page'),
    path('logout/', views.FishingLogoutView.as_view(), name='logout_page'),
    path('edit/', views.update_profile, name='profile_edit'),
    path('profile_page/<int:pk>/', views.ProfileDetailView.as_view(), name='profile'),
    path('tags/', views.tag_list, name='tags_page'),
    path('tags/<str:slug>', views.tag_detail, name='tag_detail'),
    path('tag/create', views.TagCreate.as_view(), name='tag_create'),
    path('tag/<str:slug>/update/', views.TagUpdate.as_view(), name='tag_update'),
    path('tag/<str:slug>/delete/', views.TagDelete.as_view(), name='tag_delete'),

]
