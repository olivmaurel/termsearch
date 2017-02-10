from django.contrib import admin

from .models import Website, Language, Domain, Search
# Register your models here.

admin.site.register(Website)
admin.site.register(Language)
admin.site.register(Domain)
admin.site.register(Search)