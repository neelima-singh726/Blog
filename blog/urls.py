from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('create/', views.CreatePostView.as_view(), name='post-create'),
    path('edit/<int:id>/', views.EditPostView.as_view(), name='post-edit'),
    path('delete/<int:id>/', views.DeletePostView.as_view(), name='post-delete'),
    path('send-email/', views.SendEmailView.as_view(), name='send-email'),

]
