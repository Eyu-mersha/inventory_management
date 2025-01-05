from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from django.contrib import messages
from django.urls import reverse
from inventorymgmt import models,forms
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    title = "Welcome to the homepage"
    context = {
        "title": title,
    }
    return render(request, "home.html", context)
@login_required
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
@login_required
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
		item.receive_quantity = 0
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
		item.issue_quantity = 0
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
def reorder_level(request, pk):
	queryset = models.Stock.objects.get(id=pk)
	form = forms.ReorderLevelForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(instance.reorder_level))

		return redirect("/list_items")
	context = {
			"instance": queryset,
			"form": form,
		}
	return render(request, "add_items.html", context)
@login_required
def list_history(request):
	header = 'LIST OF ITEMS'
	queryset = models.StockHistory.objects.all()
	form = forms.StockHistorySearchForm(request.POST or None)
	context = {
		"header": header,
		"queryset": queryset,
		"form":form,
	}
	if request.method == 'POST':
		catagory = form['catagory'].value()
		queryset = models.StockHistory.objects.filter(
			item_name__icontains=form['item_name'].value(),
						last_updated__range=[
												form['start_date'].value(),
												form['end_date'].value()
											]
	)
		if (catagory != ''):
			queryset = queryset.filter(catagory_id=catagory)
		if form['export_to_CSV'].value() == True:
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
			writer = csv.writer(response)
			writer.writerow(
				['CATAGORY', 
				'ITEM NAME',
				'QUANTITY', 
				'ISSUE QUANTITY', 
				'RECEIVE QUANTITY', 
				'RECEIVE BY', 
				'ISSUE BY', 
				'LAST UPDATED'])
			instance = queryset
			for stock in instance:
				writer.writerow(
				[stock.catagory, 
				stock.item_name, 
				stock.quantity, 
				stock.issue_quantity, 
				stock.receive_quantity, 
				stock.receive_by, 
				stock.issue_by, 
				stock.last_updated])
			return response

		context = {
		"form": form,
		"header": header,
		"queryset": queryset,
	}
	return render(request, "list_history.html",context)