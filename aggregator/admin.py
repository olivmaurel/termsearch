from django.contrib import admin

from .models import Website, Language, Domain
# Register your models here.

admin.site.register(Website)
admin.site.register(Language)
admin.site.register(Domain)