import django.db.models
from django.contrib import admin
import apps.adverts.models as md

from martor.widgets import AdminMartorWidget

from apps.adverts.models import Post


class YourModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        django.db.models.TextField: {'widget': AdminMartorWidget},
    }


admin.site.register(Post, YourModelAdmin)
admin.site.register(md.Author)
