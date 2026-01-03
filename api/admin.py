from django.contrib import admin
from api.models import User, UserConfirmation

admin.site.register({User, UserConfirmation})
