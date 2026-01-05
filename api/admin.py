from django.contrib import admin
from api.models import User, UserConfirmation, Post, Comment, Media

admin.site.register({User, UserConfirmation, Post, Comment, Media})
