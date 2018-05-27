from django.test import TestCase
from django.urls import reverse
from django.core.files import File

from django.conf import settings
from .models import NerString

import os

test_asset_path = os.path.join(settings.BASE_DIR, '../test_assets')

# Create your tests here.
class ClassifyViewTests(TestCase):

	def test_index(self):
		response = self.client.get(reverse('classify:index'))
		self.assertIs(response.status_code, 200)

	def test_index_empty_post(self):
		response = self.client.post(reverse('classify:index'))
		self.assertContains(response, '<ul class="errorlist">')
		self.assertIs(response.status_code, 200)

	def test_index_invalid_file_post(self):
		with open(os.path.join(test_asset_path, 'image.png'), 'rb') as file:
			response = self.client.post(reverse('classify:index'), {'file': file})
			self.assertIs(response.status_code, 200)
			self.assertContains(response, '<li>Invalid file extension</li>')

	def test_index_valid_file_post(self):
		with open(os.path.join(test_asset_path, 'test.csv')) as file:
			response = self.client.post(reverse('classify:index'), {'file': file})
			self.assertRedirects(response, reverse('classify:classify'))
			string_set = NerString.objects.all()
			self.assertIs(string_set.count(), 3)

	def test_classify_empty_db(self):
		response = self.client.get(reverse('classify:classify'))
		self.assertIs(response.status_code, 200)
		self.assertContains(response, '<h2>No records found</h2>')

	def test_classify_completed_db(self):
		with open(os.path.join(test_asset_path, 'test.csv')) as file:
			response = self.client.post(reverse('classify:index'), {'file': file})
			for record in NerString.objects.all():
				record.correct_status = True
				record.save()
			response = self.client.get(reverse('classify:classify'))
			self.assertIs(response.status_code, 200)
			self.assertContains(response, '<h2>All strings classified</h2>')

	def test_export(self):
		response = self.client.get(reverse('classify:export'))
		self.assertIs(response.status_code, 200)