from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Product Name, Reference or SKU', max_length=100)
