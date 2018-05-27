from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.files import File

from .models import NerString
from .forms import UploadFileForm, NerStringForm
from .helper_functions import handle_file_upload, sentence_split, purge_check
from django.conf import settings

import random
import csv
import os

# Create your views here.
def index(request):
	"""
	Normal GET requests will just cause it to offer a field to upload CSVs
	POST requests will cause it to parse the submitted CSV
	"""
	context = {}
	purge_check()
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_file_upload(request.FILES['file'])
			return HttpResponseRedirect(reverse('classify:classify'))
	else:
		form = UploadFileForm()			

	context['form'] = form
	return render(request, 'classify/index.html', context)

def classify(request):
	"""
	GET requests will return a NerString that is to be classified
	POST requests will register a NerString classification form submission
	"""
	context = {}
	purge_check()
	if request.method == 'POST':
		ner_string = get_object_or_404(NerString, pk=request.POST['id'])
		form = NerStringForm(request.POST, instance=ner_string)
		if form.is_valid:
			form.save()
			return HttpResponseRedirect(reverse('classify:classify'))

	# Get random NerString
	try:
		ner_string_set = NerString.objects.filter(correct_status=None)
		random_ner_string = random.choice(ner_string_set)
		context['object'] = random_ner_string

		# Split sentence into relevant 3 parts
		context['string_first'], \
		context['string_highlight'], \
		context['string_last'] = sentence_split(random_ner_string)
	except:
		if NerString.objects.all().exists():
			# There are records in the DB
			context['status'] = 'done'
		else:
			# The DB is empty, should upload something first
			context['status'] = 'empty'
	return render(request, 'classify/classify.html', context)

def export(request):
	"""
	GET request just offers a page with a download button
	POST offers a download
	"""
	purge_check()
	context = {}
	if request.method == 'POST':
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="classifr_export.csv"'
		records = NerString.objects.exclude(correct_status=None)
		writer = csv.writer(response)

		# Write header
		writer.writerow(['String', 'Classification status', 'timestamp'])

		for record in records:
			writer.writerow([record.string_text, record.correct_status, record.last_edit])

		return response
	return render(request, 'classify/export.html', context)

def demo(request):
	purge_check()
	file_path = os.path.join(settings.BASE_DIR, '../test_assets', 'test.csv')
	with open(file_path, 'rb') as file_handle:
		django_file_object = File(file_handle)
		handle_file_upload(django_file_object)
		return HttpResponseRedirect(reverse('classify:classify'))