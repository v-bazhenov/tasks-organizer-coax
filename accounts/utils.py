from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_max_age(value):
    if value >= 100:
        raise ValidationError(
            _('%(value)s is greater than 100. Please enter the value from 0 to 100.'),
            params={'value': value},
        )
