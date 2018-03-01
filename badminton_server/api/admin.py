from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Interested)
admin.site.register(Member)
admin.site.register(BoardMember)
admin.site.register(Queue)
admin.site.register(Court)
admin.site.register(Tournament)