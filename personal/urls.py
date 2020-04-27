from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns =[
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('blog/',views.blog,name='blog'),
    path('gallery/',views.gallery,name='gallery'),
    path('codesnippets/',views.codesnippets,name='codesnippets'),
    path('downloads/',views.downloads,name='downloads'),
    path('acknlg/',views.acknlg,name='acknlg'),
    path('notes/',views.notes,name='notes'),
    path('search_result/',views.search_result,name='search_result'),
    path('signup/',views.signup,name='signup'),
    path('chat_board/',views.chat_board,name='chat_board'),
    path('profile/',views.profile,name='profile'),
    path('post/',views.post,name='post'),
    path('logout/', auth_views.LogoutView.as_view(template_name='personal/blog.html'), name='logout'),
    path('user_detail/', views.user_detail, name='user_detail'),
    path('edit_post/',views.edit_post,name='edit_post'),
    path('create_post/',views.create_post,name='create_post'),
]