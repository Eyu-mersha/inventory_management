from django import forms
from .models import Stock


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

class StockSearchForm(forms.ModelForm):
   class Meta:
     model = Stock
     fields = ['catagory', 'item_name']

class StockUpdateForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['catagory', 'item_name', 'quantity']