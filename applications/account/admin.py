from django.contrib import admin

from applications.account.models import CustomUser

admin.site.register(CustomUser)
