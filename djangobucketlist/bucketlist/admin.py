from django.contrib import admin
from .models import BucketList, BucketlistItem


class BucketItems(admin.TabularInline):
    model = BucketlistItem


class BucketListAdmin(admin.ModelAdmin):
    inlines = [BucketItems]
    list_display = ('name', 'date_created', 'date_modified')

admin.site.register(BucketList, BucketListAdmin)
