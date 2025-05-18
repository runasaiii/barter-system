from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('<int:pk>/', views.ad_detail, name='ad_detail'),
    path('create/', views.create_ad, name='create_ad'),
    path('edit/<int:pk>/', views.edit_ad, name='edit_ad'),
    path('delete/<int:pk>/', views.delete_ad, name='delete_ad'),
    path('<int:ad_id>/proposal/create/', views.create_proposal, name='create_proposal'),  
    path('proposals/', views.proposals_for_user, name='proposals_for_user'),
    path('proposals/<int:proposal_id>/handle/', views.handle_proposal, name='handle_proposal'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
]

