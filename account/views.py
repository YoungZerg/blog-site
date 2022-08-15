from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegisterForm, AccAuthenticationForm, AccUpdateInfoForm
from blogpost.models import BlogPost
# Create your views here.



def register_view(request):
	context = {}

	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_pass = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_pass)
			login(request, account)
			return redirect('home')
		else:
			context['registration_form'] = form
	else:
		form = RegisterForm()
		context['registration_form'] = form 
	return render(request, 'account/register.html', context)



def logout_view(request):
	logout(request)
	return redirect('home')




def login_view(request):
	context = {}

	user = request.user 

	if user.is_authenticated:
		return redirect('home')

	if request.method == 'POST':
		form = AccAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect('home')
	
	else:
		form = AccAuthenticationForm()

	context['login_form'] = form 

	return render(request, 'account/login.html', context)



def account_view(request):

	context = {}

	if not request.user.is_authenticated:
		return redirect('login')

	if request.method == 'POST':
		form = AccUpdateInfoForm(request.POST, instance = request.user)
		if form.is_valid():
			form.initial = {
				'email': request.POST['email'],
				'username': request.POST['username']

			}
			form.save()
			context['all_is_good'] = "Info Was Successfully Updated"
	else:
		form  = AccUpdateInfoForm(
			initial={
			'email': request.user.email,
			'username': request.user.username
			})

	context['account_form'] = form


	all_posts = BlogPost.objects.filter(author=request.user)
	context['all_posts'] = all_posts


	return render(request, 'account/account.html', context)



def need_authentication_view(request):
	return render(request, 'account/need_authentication.html', {})