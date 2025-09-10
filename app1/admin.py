from django.contrib import admin
from app1.models import Food,FoodCart,CustomUser
# Register your models here.

class FoodAdmin(admin.ModelAdmin):
    list_display=['id','name','img','disciption','prize']

admin.site.register(Food,FoodAdmin)
admin.site.register(FoodCart)
admin.site.register(CustomUser)
