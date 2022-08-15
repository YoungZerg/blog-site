from django.shortcuts import render
from operator import attrgetter
from blogpost.models import BlogPost
from blogpost.views import get_blog
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
BLOG_POST_PER_PAGE = 8

def home_view(request):
	context = {}
	query = ""
	if request.method == "GET":
		query = request.GET.get('q', '')
		context['query'] = str(query)


	blog_posts = sorted(get_blog(query), key=attrgetter('date_updated'), reverse=True)
	context['blog_posts'] = blog_posts


	page = request.GET.get('page', 1)
	blog_posts_pagin = Paginator(blog_posts, BLOG_POST_PER_PAGE)

	try:
		blog_posts = blog_posts_pagin.page(page)

	except PageNotAnInteger:
		blog_posts = blog_posts_pagin.page(BLOG_POST_PER_PAGE)

	except EmptyPage:
		blog_posts = blog_posts_pagin.page(blog_posts_pagin.num_pages)


	context['blog_posts'] = blog_posts

	return render(request, 'personal/home.html', context)