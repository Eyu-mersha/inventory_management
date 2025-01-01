from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from django.contrib import messages
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
    if request.method == 'POST' and form.is_valid():
        catagory_id = form.cleaned_data['catagory']  # Access the selected category from the form
        item_name = form.cleaned_data['item_name']

        # Apply filters based on user input
        if catagory_id:
            queryset = queryset.filter(catagory_id=catagory_id)  # Use category_id to filter by Category ID


        # Apply item_name filter if it's provided
        if item_name:
            queryset = queryset.filter(item_name__icontains=item_name)
        
                # CSV Export
        if form.cleaned_data.get('export_to_CSV', False):
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List_of_stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATAGORY', 'ITEM NAME', 'QUANTITY'])

            for stock in queryset:
                writer.writerow([stock.catagory.name, stock.item_name, stock.quantity])

            return response
    
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
        messages.success(request, 'Successfully ')
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

def stock_detail(request, pk):
	queryset = models.Stock.objects.get(id=pk)
	context = {
		"queryset": queryset,
	}
	return render(request, "stock_detail.html", context)

def issue_items(request, pk):
	queryset = models.Stock.objects.get(id=pk)
	form = forms.IssueForm(request.POST or None, instance=queryset)
	if form.is_valid():
		item = form.save(commit=False)
		item.quantity -= item.issue_quantity
		messages.success(request, "Issued SUCCESSFULLY. " + str(item.quantity) + " " + str(item.item_name) + "s now left in Store")
		item.save()

		return redirect('/stock_detail/'+str(item.id))


	context = {
		"title": 'Issue ' + str(queryset.item_name),
		"queryset": queryset,
		"form": form,
	}
	return render(request, "add_items.html", context)



def receive_items(request, pk):
	queryset = models.Stock.objects.get(id=pk)
	form = forms.ReceiveForm(request.POST or None, instance=queryset)
	if form.is_valid():
		item = form.save(commit=False)
		item.quantity += item.receive_quantity
		item.save()
		messages.success(request, "Received SUCCESSFULLY. " + str(item.quantity) + " " + str(item.item_name)+"s now in Store")

		return redirect('/stock_detail/'+str(item.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
	context = {
			"title": 'Receive ' + str(queryset.item_name),
			"item": queryset,
			"form": form,
		}
	return render(request, "add_items.html", context)
