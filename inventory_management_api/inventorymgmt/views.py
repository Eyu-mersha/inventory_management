from django.shortcuts import render, redirect
from django.urls import reverse
from inventorymgmt import models,forms

# Create your views here.
def home(request):
    title = "Welcome to the homepage"
    context = {
        "title": title,
    }
    return render(request, "home.html", context)

def list_items(request):
    title= "list of items in stock"
    form = forms.StockSearchForm(request.POST or None)
    queryset= models.Stock.objects.all()
    context = {
        "title": title,
        "queryset":queryset,
        "form": form,
    }
    if request.method == 'POST':
        queryset = models.Stock.objects.filter(catagory__icontains=form['catagory'].value(),
                                        item_name__icontains=form['item_name'].value()
                                        )
        context = {
        "form": form,
        "title":title,
        "queryset": queryset,
    }
    return render(request, "list_items.html", context)

def add_items(request):
    form = forms.StockCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_items')
    queryset= models.Stock.objects.all()
    context = {
        "form": form,
        "title":"Add Item",
    }
    return render(request, "add_items.html", context)
def update_items(request, pk):
	queryset = models.Stock.objects.get(id=pk)
	form = forms.StockUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = forms.StockUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			return redirect('/list_items')

	context = {
		'form':form
	}
	return render(request, 'add_items.html', context)
def delete_items(request, pk):
	queryset = models.Stock.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		return redirect('/list_items')
	return render(request, 'delete_items.html')