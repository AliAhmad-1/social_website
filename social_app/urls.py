from django.urls import path
from . import views
urlpatterns = [
    path('posts/',views.posts,name='posts'),
    path('post/create/',views.create_post,name='create'),
    path('post/delete/',views.delete_post,name='delete_post'),
    path('post/update/',views.update_post,name='update_post'),
    path('post/like/',views.like,name='like'),
    path('post/comment/',views.comment,name='comment'),
    path('post/comment/delete/',views.delete_comment,name='delete_comment'),
    path('post/comment/update/',views.update_comment,name='update_comment'),
    path('post/save/',views.save_post,name='save_post'),
    path('user/follow',views.user_follow,name='follow'),
    path('user/saves/',views.saves,name='saves'),
    path('user/following/',views.following,name='following'),
    path('users/search/',views.search,name='search')

]
