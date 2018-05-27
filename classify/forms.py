from django import forms
from django.forms import ValidationError
from .models import NerString

import os

class CsvFileField(forms.FileField):
	def validate(self, value):
		super().validate(value)
		# print(value.temporary_file_path())
		file_extension = os.path.splitext(value.name)[1]
		if file_extension != '.csv':
			raise ValidationError(
				('Invalid file extension'),
				code='invalid'
			)

class UploadFileForm(forms.Form):
    file = CsvFileField()

class NerStringForm(forms.ModelForm):
	class Meta:
		model = NerString
		fields = ['id', 'correct_status']