from django.contrib import admin
from users.models import Friendship


class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followed')


# admin.site.register(Friendship, FriendshipAdmin)
