from django.core.exceptions import ValidationError


def validate_image_size(value):
	if value:
		if value.size > 5*1024*1024:
			raise ValidationError("The image size should be less than 5 mb")
			return value
	else:
		raise ValidationError("Couldn't read uploaded image")