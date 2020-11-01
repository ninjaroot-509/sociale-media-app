from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Art)
admin.site.register(Comments)
admin.site.register(Commentposts)
admin.site.register(Like)
admin.site.register(Category)