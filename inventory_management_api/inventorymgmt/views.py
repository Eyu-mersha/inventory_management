from django.shortcuts import render

from inventorymgmt import models,forms

# Create your views here.
def home(request):
    title = "Welcome to the homepage"
    context = {
        "title": title,
    }
    return render(request, "home.html", context)

def list_items(request):
    title = "list of items in stock"
    queryset= models.Stock.objects.all()
    context = {
        "title": title,
        "queryset":queryset,
    }
    return render(request, "list_items.html", context)
def add_items(request):
    form = forms.StockCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
    queryset= models.Stock.objects.all()
    context = {
        "form": form,
        "title":"Add Item",
    }
    return render(request, "add_items.html", context)