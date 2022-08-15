from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
# Register your models here.



class AdminAccount(UserAdmin):
	list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
	search_fields = ('email', 'username')
	readonly_fields = ('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ('is_admin',)
	fieldsets = ()
	ordering = ('email',)

admin.site.register(Account, AdminAccount)