from django.db import models

# Create your models here.
class NerString(models.Model):
	string_text = models.CharField(max_length=200)
	ne_start_char = models.PositiveSmallIntegerField()
	ne_end_char = models.PositiveSmallIntegerField()
	ne_type = models.CharField(max_length=200)

	# Filled out by default
	INCORRECT = 0
	CORRECT = 1
	NER_CHOICES = (
		(INCORRECT, 'Incorrect'),
		(CORRECT, 'Correct')
	)

	correct_status = models.NullBooleanField(
		null=True,
		choices=NER_CHOICES,
	)
	last_edit = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.string_text