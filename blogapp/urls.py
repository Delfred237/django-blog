from django.urls import path
from . import views

app_name = 'blogapp'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('article/create/', views.create_article_view, name='create_article'),
    path('article/<int:pk>/', views.detail_article_view, name='detail_article'),
    path('article/<int:pk>/modify/', views.modify_article_view, name='modify_article'),
    path('article/<int:pk>/delete/', views.delete_article_view, name='delete_article'),

    path('article/<int:article_pk>/comment/', views.add_comment_view, name='add_comment'),

    path('profile/<str:username>/', views.user_profile_view, name='user_profile')
]