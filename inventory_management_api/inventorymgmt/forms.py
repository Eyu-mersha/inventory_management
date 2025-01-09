from django import forms
from .models import Stock
from .models import Catagory ,StockHistory
from django.contrib.auth.models import User

class StockCreationForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['catagory','item_name','quantity','price','description']
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
    def clean_quantity(self):
      quantity = self.cleaned_data.get('quantity')
      if quantity == 0:
        raise forms.ValidationError('This field is required')
      return quantity
    def clean_price(self):
      price = self.cleaned_data.get('price')
      if price == 0.00:
        raise forms.ValidationError('This field is required')
      return price

class CatagoryCreationForm(forms.ModelForm):
    class Meta:
        model = Catagory
        fields = ['name']
    def clean_name(self):
        catagory_name = self.cleaned_data.get('name')
        
        if not catagory_name:
            raise forms.ValidationError('This field is required')
        
        # Check if the category already exists
        if Catagory.objects.filter(name=catagory_name).exists():
            raise forms.ValidationError(f'"{catagory_name}" category already exists')
        
        return catagory_name

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match")
        return password_confirmation

class StockSearchForm(forms.Form):  # Use a regular form for search (not ModelForm)
    
    catagory = forms.ModelChoiceField(queryset=Catagory.objects.all(), required=False, empty_label="All Categories")
    item_name = forms.CharField(required=False)
    min_price = forms.DecimalField(required=False, max_digits=10, decimal_places=2, label='Min Price', widget=forms.NumberInput(attrs={'step': '0.01'}))
    max_price = forms.DecimalField(required=False, max_digits=10, decimal_places=2, label='Max Price', widget=forms.NumberInput(attrs={'step': '0.01'}))
    export_to_CSV = forms.BooleanField(required=False)
    Short_stocks = forms.BooleanField(required=False)
    
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