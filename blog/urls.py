from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Auth
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Profil
    path('profile/', views.profile, name='profile'),

    # Posts
    path('post/add/', views.add_post, name='add_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),

    # Like + Comment
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),

    # Catégories
    path('category/<int:category_id>/', views.category_posts, name='category_posts'),

    # Mes articles
    path('my_posts/', views.my_posts, name='my_posts'),

    # Admin
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/categories/', views.admin_categories, name='admin_categories'),
    path('dashboard/categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('dashboard/users/', views.admin_users, name='admin_users'),
    path('dashboard/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
]