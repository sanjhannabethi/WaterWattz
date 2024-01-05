from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('household', _('Household')),
        ('industry', _('Industry')),
        ('municipal', _('Municipal')),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    # Add other profile fields as needed
