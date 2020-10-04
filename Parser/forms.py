import io
from django import forms
import csv


class UploadFileForm(forms.Form):

    file = forms.FileField()

    def process_data(self):
        f = io.TextIOWrapper(self.cleaned_data['file'].file)
        reader = csv.DictReader(f)
        print(reader)