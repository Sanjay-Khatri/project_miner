from django.contrib import admin
from product_app.models import *
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reaction)
