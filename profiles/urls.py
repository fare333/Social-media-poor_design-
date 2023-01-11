from django.urls import path

from . import views

urlpatterns = [
	path("my_profile/",views.my_profile,name="my_profile"),
 	path("<str:pk>/",views.get_profiles,name="get_profiles"),
    path("search",views.search,name="search"),
    path("add-follow/<str:pk>/",views.add_follow,name="add_follow"),
    path("p/get_all_profiles/",views.get_all_profiles,name="all_profiles"),
    path("p/edit_profile/",views.edit_profile,name="edit_profile"),
    path("p/all_user_followers",views.all_user_followers,name="all_user_followers"),
    path("p/user_followers/<str:pk>/",views.user_followers,name="user_followers")
]