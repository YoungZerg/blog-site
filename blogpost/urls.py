from django.urls import path 
from blogpost.views import create_blog_view, detail_blog_view, update_blog_post_view


app_name = 'blogpost'


urlpatterns = [

	path('create/', create_blog_view, name='create'),
	path('<slug>/', detail_blog_view, name='detail'),
	path('<slug>/edit', update_blog_post_view, name="update")
	
]