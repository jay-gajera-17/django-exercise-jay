from django.contrib import admin
from .models import  Question,Choice,Vote
from .models import CustomUser


admin.site.register(Question)
admin.site.register(CustomUser)
admin.site.register(Choice)
admin.site.register(Vote)

# Register your models here.
