from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Interested)
admin.site.register(Member)
admin.site.register(BoardMember)
admin.site.register(Election)
admin.site.register(Announcement)
admin.site.register(Match)
admin.site.register(FinishedMatch)
admin.site.register(Team)