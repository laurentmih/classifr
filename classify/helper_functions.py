import csv
import datetime

from django.core import management

from .models import NerString

def handle_file_upload(file):
	for chunk in file.chunks():
		cleaned_chunk = chunk.decode('utf-8').split('\n')
		reader = csv.reader(cleaned_chunk, delimiter=',')
		for row in reader:
			if len(row) > 0:
				string = row[0]
				start_char = row[1].replace(" ", "")
				end_char = row[2].replace(" ", "")
				ne_type = row[3].replace(" ", "")

				new_object = NerString(
						string_text = string,
						ne_start_char = start_char,
						ne_end_char = end_char,
						ne_type = ne_type,
					)

				new_object.save()

def sentence_split(ner_string_object):
	text = ner_string_object.string_text
	start = ner_string_object.ne_start_char
	end = ner_string_object.ne_end_char
	text_length = len(text)

	first_part = text[0:start]
	ne_part = text[start:end+1]
	last_part = text[end+1:text_length]

	return first_part, ne_part, last_part

def purge_check():
	# management.call_command('flush', interactive=False)
	# maintenance stuff for running in demo
	ner_string_query_set = NerString.objects.all().exclude(last_edit__date=datetime.date.today())
	try:
		for record in ner_string_query_set:
			record.delete()
	except:
		pass