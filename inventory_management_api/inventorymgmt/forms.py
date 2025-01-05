from django import forms
from .models import Stock
from .models import Catagory ,StockHistory



class StockCreationForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['catagory','item_name','quantity']
    def clean_category(self):
      catagory = self.cleaned_data.get('catagory')
      if not catagory:
        raise forms.ValidationError('This field is required')
      for item in Stock.objects.all():
         if item.catagory == catagory:
            raise forms.ValidationError(catagory + 'is already created')
      return catagory
    def clean_item_name(self):
      item_name = self.cleaned_data.get('item_name')
      if not item_name:
        raise forms.ValidationError('This field is required')
      return item_name


class StockSearchForm(forms.Form):  # Use a regular form for search (not ModelForm)
    
    catagory = forms.ModelChoiceField(queryset=Catagory.objects.all(), required=False, empty_label="All Categories")
    item_name = forms.CharField(required=False)
    export_to_CSV = forms.BooleanField(required=False)

class StockHistorySearchForm(forms.ModelForm):
	export_to_CSV = forms.BooleanField(required=False)
	start_date = forms.DateTimeField(required=False)
	end_date = forms.DateTimeField(required=False)
	class Meta:
		model = StockHistory
		fields = ['catagory', 'item_name', 'start_date', 'end_date']

class StockUpdateForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['catagory', 'item_name', 'quantity']
        
class IssueForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['issue_quantity', 'issue_to']


class ReceiveForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['receive_quantity']
          
class ReorderLevelForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['reorder_level']