from django.contrib import admin
from .models import User, Note, Audio, Sentence

# Register your models here.
admin.site.register(User)
admin.site.register(Note)
admin.site.register(Audio)
admin.site.register(Sentence)