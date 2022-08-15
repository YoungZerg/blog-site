from django.shortcuts import render, redirect, get_object_or_404
from blogpost.models import BlogPost
from blogpost.forms import BlogPostForm, UpdateBlogPostForm
from account.models import Account
from django.db.models import Q
from django.http import HttpResponse

# Create your views here.



def create_blog_view(request):
	context = {}
	user = request.user

	if not user.is_authenticated:
		return redirect('need_authentication')


	form = BlogPostForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email = user.email).first()
		obj.author = author
		obj.save()
		form = BlogPostForm()


	context['form'] = form 


	return render(request, 'blogpost/create_blog.html', context)



def detail_blog_view(request, slug):


	blog_post = get_object_or_404(BlogPost, slug=slug)

	context = {'blog_post': blog_post}


	return render(request, 'blogpost/detail_blog.html', context)





def update_blog_post_view(request, slug):
	context = {}

	user = request.user

	if not user.is_authenticated:
		return redirect('need_authentication')

	blog_post = get_object_or_404(BlogPost, slug=slug)

	if blog_post.author != user:
		return HttpResponse("You're not allowed to edit that post.")

	if request.method == 'POST':
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_mess'] = "Post was updated"
			blog_post = obj
	form = UpdateBlogPostForm(
			initial = {
				'title': blog_post.title,
				'body': blog_post.body,
				'image': blog_post.image,
			}
		)


	context['form'] = form


	return render(request,'blogpost/edit_blog.html', context)



def get_blog(query=None):
	queryset = []
	queries =query.split(" ")

	for q in queries:
		posts = BlogPost.objects.filter(
				Q(title__icontains=q) |
				Q(body__icontains=q)

			).distinct()

		for post in posts:
			 queryset.append(post)


	return list(set(queryset))