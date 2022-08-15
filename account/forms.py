from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account



class RegisterForm(UserCreationForm):
	email = forms.EmailField(max_length=100, help_text='Required field. Please add a valid email')
	
	class Meta:
		model = Account
		fields = ['email', 'username', 'password1', 'password2']




class AccAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ['email', 'password']


	def clean(self):

		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Error: please be sure your input is correct")





class AccUpdateInfoForm(forms.ModelForm):


	class Meta:
		model = Account
		fields = ['email', 'username']


	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			try:
				account = Account.objects.exclude(pk = self.instance.pk).get(email=email)
			except Account.DoesNotExist:
				return email
			raise forms.ValidationError(f"Email {account.email} already exists.")


	def clean_username(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			try:
				account = Account.objects.exclude(pk = self.instance.pk).get(username=username)
			except Account.DoesNotExist:
				return username
			raise forms.ValidationError(f"This username '{account.username}' already exists.")