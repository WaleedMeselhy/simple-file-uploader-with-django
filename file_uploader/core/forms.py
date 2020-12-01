from django import forms


class SearchForm(forms.Form):
    file_name = forms.CharField(label="file name", max_length=100)
