from django.urls import path 
from .views import CreateBlog , BlogManagement , PostEdit , PostsHasBlog , BlogView , PostDetail  , SearchPage
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(CreateBlog.as_view() , login_url='login') ,name='create-blog'),

    path('manage-blog', login_required(BlogManagement.as_view() , login_url='login') ,name='blog-management'),

    path('manage-blog/posts', login_required(PostsHasBlog.as_view() , login_url='login') ,name='posts-has-blog'),

    path('manage-blog/<int:id>/edit', login_required(PostEdit.as_view() , login_url='login') ,name='post-edit'),

    path('<str:slug>/', BlogView.as_view()  ,name='blog-view'),

    path('<str:blog>/<str:slug>/<int:id>/', PostDetail.as_view()  ,name='post-view'),

    path('<str:slug>/search/', SearchPage.as_view() , name='search'),
]