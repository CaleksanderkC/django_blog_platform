from django.contrib import admin
from django.urls import include, path

from theme.views import RedirectLike,, PostListView
from theme import views


app_name = 'theme'

urlpatterns = [
    path('', views.index, name='index'),
    path('creat_post', views.creat, name='creat'),
    path('<str:slug>/', views.detail, name='detail'),
    path('<str:slug>/edit', views.edit, name='edit'),
    path('<int:comment_id>/del-comment', views.delete_own_comment, name='del_comment'),
    path('<str:slug>/del-post', views.delete_own_post, name='del_post'),
    path('<str:slug>/like', RedirectLike.as_view(), name='like-toggle'),
    path('art', PostListView.as_view(), name='article-list'),

]
