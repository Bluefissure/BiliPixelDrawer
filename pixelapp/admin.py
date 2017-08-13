from django.contrib import admin
from .models import *
# Register your models here.
class PixelAdmin(admin.ModelAdmin):
    list_display = ('x','y','color','project','updtime','finuser')
    list_filter = ('project','finuser')
admin.site.register(User)
admin.site.register(Project)
admin.site.register(Token)
admin.site.register(Pixel,PixelAdmin)