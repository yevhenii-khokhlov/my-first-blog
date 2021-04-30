from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostList.as_view(template_name="blog/post_list.html"), name='post-list'),
    path('post/<int:pk>/',
         views.PostDetailView.as_view(template_name="blog/post_detail.html"),
         name='post-detail'
         ),
    path('post/new/', views.post_new, name='post-new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post-edit'),
    path('post/<int:post_id>/comment/new/', views.CommentNewView.as_view(), name='comment-new'),
    path('about/', views.about, name='about'),
]
