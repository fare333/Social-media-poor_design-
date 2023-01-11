from django.urls import path

from . import views

urlpatterns = [
	path('posts/', views.get_all_posts, name='get_all_posts'),
	path("delete/<str:pk>/",views.delete_post,name="delete_post"),
	path("update/<str:pk>/",views.update_post,name="update_post"),
	path("delete_comment/<str:pk>/",views.delete_comment,name="delete_comment"),
	path("post_detail/<str:pk>/",views.post_detail,name="post_detail"),
	path("add-like/",views.add_like,name="add_like"),
]