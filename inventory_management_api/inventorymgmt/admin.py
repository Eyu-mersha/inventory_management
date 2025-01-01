from django.contrib import admin
from .forms import StockCreationForm
from .models import Stock,Catagory

# Register your models here. c
 
class StockCreateAdmin(admin.ModelAdmin):
    list_display = ['catagory', 'item_name', 'quantity']
    form=StockCreationForm
    list_filter= ['catagory']
    search_fields =['catagory','item_name']


admin.site.register(Stock,StockCreateAdmin)
admin.site.register(Catagory)